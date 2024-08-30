import requests
from django.contrib import admin
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from settings import TELEGRAM_BOT_TOKEN
from settings import TELEGRAM_CHAT_IDS
from settings import LOG_SIZE


class Monitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    su_host = models.CharField(max_length=255, null=True, blank=True)
    su_port = models.PositiveIntegerField(default=22)
    su_login = models.CharField(max_length=255, null=True, blank=True)
    su_password = models.CharField(max_length=255, null=True, blank=True)
    su_restore_commands = models.TextField(null=True, blank=True)
    restore_hops = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.host}:{self.port}"

    @classmethod
    def change_commands_syntax(cls, sender, instance, created, *args, **kwargs):
        instance.su_restore_commands = ";".join(
            [x.strip() for x in instance.su_restore_commands.split("\n")]
        )
        signals.post_save.disconnect(Monitor.change_commands_syntax, sender=Monitor)
        instance.save()
        signals.post_save.connect(Monitor.change_commands_syntax, sender=Monitor)


signals.post_save.connect(Monitor.change_commands_syntax, sender=Monitor)


class MonitorActivity(models.Model):
    monitor = models.ForeignKey("monitoring.Monitor", on_delete=models.CASCADE)
    server_response = models.CharField(max_length=255, null=True, blank=True)
    server_available = models.BooleanField(default=True)
    creation_date = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.monitor} {self.server_response}"

    class Meta:
        ordering = ["-id"]

    def restore_hops(self):
        return self.monitor.restore_hops

    restore_hops.admin_order_field = "monitor__restore_hops"

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % LOG_SIZE == 0):
            MonitorActivity.objects.all().delete()


signals.post_save.connect(MonitorActivity.check_stat_size, sender=MonitorActivity)


class RestoreActivity(models.Model):
    monitor = models.ForeignKey("monitoring.Monitor", on_delete=models.CASCADE)
    console_log = models.TextField(null=True, blank=True)
    exit_status = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.monitor}"

    class Meta:
        ordering = ["-id"]

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % LOG_SIZE == 0):
            RestoreActivity.objects.all().delete()

    @classmethod
    def send_notify_to_telegram_bot(cls, sender, instance, created, *args, **kwargs):
        text = f"Restore activity: {instance.monitor}\n\nRestore log{instance.console_log}\n\nExit status:{instance.exit_status}"
        for chat_id in TELEGRAM_CHAT_IDS:
            requests.post(
                url="https://api.telegram.org/bot{}/{}".format(
                    TELEGRAM_BOT_TOKEN, "sendMessage"
                ),
                data={"chat_id": chat_id, "text": text},
            )


signals.post_save.connect(RestoreActivity.check_stat_size, sender=RestoreActivity)
signals.post_save.connect(
    RestoreActivity.send_notify_to_telegram_bot, sender=MonitorActivity
)
