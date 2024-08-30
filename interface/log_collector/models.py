import traceback
from loguru import logger
from simple_print import sprint
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from settings import LOG_SIZE
from settings import ALERTS
from settings import DEBUG
from settings import PROD
from django.forms.models import model_to_dict
import __upserver__


class AnyLogger(models.Model):
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    payload = models.JSONField()
    tag = models.CharField(max_length=255)
    routing_key = models.CharField(max_length=255)
    ttl = models.PositiveIntegerField(default=1)
    filename = models.CharField(max_length=255, null=True, blank=True)
    function_name = models.CharField(max_length=255, null=True, blank=True)
    lineno = models.PositiveIntegerField(default=1)
    send_datetime = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Any Logger")
        verbose_name_plural = _("Any Logger")

    def __str__(self):
        return f"{self.tag}"

    @classmethod
    def save_record(cls, row):
        from log_collector.schema import AnyLoggerSchema

        logger.info(AnyLogger.save_record.__qualname__)

        fn_data = f"{row}"
        save = True

        try:
            row = AnyLoggerSchema(**row).dict()
        except Exception as error:
            if PROD:
                exc_info = traceback.format_exception(error)
                exc_info = "\n".join(exc_info)
                collector_exception = CollectorException()
                collector_exception.fn_name = sprint("schema error", s=1)
                collector_exception.fn_data = fn_data
                collector_exception.exc_info = exc_info
                collector_exception.save()
                save = False

            if DEBUG:
                sprint(error, c="red", p=1)
                raise Exception("AnyLogger schema error")

            if ALERTS:
                __upserver__.any_throw(
                    {"error": sprint(error, s=1)}, routing_key="alerts"
                )

        if save:
            record = AnyLogger()
            for field in cls._meta.fields:
                field_name = field.name
                if field_name in row and row[field_name]:
                    setattr(record, field_name, row[field_name])
            try:
                record.save()

                if ALERTS:
                    __upserver__.any_throw(model_to_dict(record), routing_key="alerts")

                if DEBUG:
                    sprint("Record save [OK]", c="green", p=1)

            except Exception as error:
                if PROD:
                    exc_info = traceback.format_exception(error)
                    exc_info = "\n".join(exc_info)
                    collector_exception = CollectorException()
                    collector_exception.fn_name = sprint("model save error", s=1)
                    collector_exception.fn_data = fn_data
                    collector_exception.exc_info = exc_info
                    collector_exception.save()

                if ALERTS:
                    __upserver__.any_throw(
                        {"error": sprint(error, s=1)}, routing_key="alerts"
                    )

                if DEBUG:
                    sprint(error, c="red", p=1)
                    raise Exception("AnyLogger save error")

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % LOG_SIZE == 0):
            AnyLogger.objects.all().delete()


post_save.connect(AnyLogger.check_stat_size, sender=AnyLogger)


class DjangoLogger(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "new", _("New")
        IN_PROCCESS = "in_proccess", _("In proccess")
        RESOLVED = "resolved", _("Resolved")
        NOT_RESOLVED = "not_resolved", _("Not resolved")

    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=24, choices=StatusChoices.choices, default=StatusChoices.NEW
    )
    errors_count = models.PositiveIntegerField(default=0)
    asctime = models.DateTimeField(auto_now_add=True)
    exc_info = models.TextField(null=True, blank=True)
    exc_hash = models.CharField(max_length=255, unique=True)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    user = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField(default=22, null=True, blank=True)
    request_extra = models.TextField(null=True, blank=True)
    site = models.CharField(max_length=255, null=True, blank=True)
    scheme = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=255, null=True, blank=True)
    GET = models.TextField(null=True, blank=True)
    POST = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    args = models.TextField(null=True, blank=True)
    kwargs = models.TextField(null=True, blank=True)
    pathname = models.CharField(max_length=255, null=True, blank=True)
    funcName = models.CharField(max_length=255, null=True, blank=True)
    lineno = models.PositiveIntegerField(default=1)
    message = models.CharField(max_length=255, null=True, blank=True)
    exc_text = models.CharField(max_length=255, null=True, blank=True)
    created = models.FloatField(null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)
    levelname = models.CharField(max_length=255, null=True, blank=True)
    levelno = models.CharField(max_length=255, null=True, blank=True)
    module = models.CharField(max_length=255, null=True, blank=True)
    msecs = models.FloatField(default=22)
    msg = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    process = models.CharField(max_length=255, null=True, blank=True)
    processName = models.CharField(max_length=255, null=True, blank=True)
    relativeCreated = models.CharField(max_length=255, null=True, blank=True)
    stack_info = models.CharField(max_length=255, null=True, blank=True)
    thread = models.CharField(max_length=255, null=True, blank=True)
    threadName = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Django Errors")
        verbose_name_plural = _("Django Errors")

    def __str__(self):
        return f"{self.message}"

    @classmethod
    def save_record(cls, row):
        from log_collector.schema import DjangoLoggerSchema

        fn_data = f"{row}"
        payload = row["payload"]
        save = True

        try:
            payload = DjangoLoggerSchema(**payload).dict()
        except Exception as error:
            if PROD:
                exc_info = traceback.format_exception(error)
                exc_info = "\n".join(exc_info)
                collector_exception = CollectorException()
                collector_exception.fn_name = sprint("schema error", s=1)
                collector_exception.fn_data = fn_data
                collector_exception.exc_info = exc_info
                collector_exception.save()
                save = False

            if ALERTS:
                __upserver__.any_throw(
                    {"error": sprint(error, s=1)}, routing_key="alerts"
                )

            if DEBUG:
                sprint(error, c="red", p=1)
                raise Exception("DjangoLogger schema error")

        if save:
            record_check = DjangoLogger.objects.filter(
                exc_hash=payload["exc_hash"]
            ).first()
            if record_check:
                record_check.errors_count += 1
                record_check.save()

                if record_check.errors_count % 50 == 0 and ALERTS:
                    __upserver__.any_throw(
                        model_to_dict(record_check), routing_key="alerts"
                    )

            else:
                record = DjangoLogger()
                for field in cls._meta.fields:
                    field_name = field.name
                    if field_name in payload and payload[field_name]:
                        setattr(record, field_name, payload[field_name])
                try:
                    record.save()

                    if ALERTS:
                        __upserver__.any_throw(
                            model_to_dict(record), routing_key="alerts"
                        )

                    if DEBUG:
                        sprint("Record save [OK]", c="green", p=1)

                except Exception as error:
                    if PROD:
                        exc_info = traceback.format_exception(error)
                        exc_info = "\n".join(exc_info)
                        collector_exception = CollectorException()
                        collector_exception.fn_name = sprint("model save error", s=1)
                        collector_exception.fn_data = fn_data
                        collector_exception.exc_info = exc_info
                        collector_exception.save()

                    if ALERTS:
                        __upserver__.any_throw(
                            {"error": sprint(error, s=1)}, routing_key="alerts"
                        )

                    if DEBUG:
                        sprint(error, c="red", p=1)
                        raise Exception("DjangoLogger save error")

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % LOG_SIZE == 0):
            DjangoLogger.objects.all().delete()


post_save.connect(DjangoLogger.check_stat_size, sender=DjangoLogger)


class DjangoException(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = "new", _("New")
        IN_PROCCESS = "in_proccess", _("In proccess")
        RESOLVED = "resolved", _("Resolved")
        NOT_RESOLVED = "not_resolved", _("Not resolved")

    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=24, choices=StatusChoices.choices, default=StatusChoices.NEW
    )
    errors_count = models.PositiveIntegerField(default=0)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    asctime = models.DateTimeField(auto_now_add=True)
    exc_info = models.TextField(null=True, blank=True)
    exc_hash = models.CharField(max_length=255, unique=True)
    message = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Captured Exceptions (Sentry like)")
        verbose_name_plural = _("Captured Exceptions (Sentry like)")

    def __str__(self):
        return f"{self.message}"

    @classmethod
    def save_record(cls, row):
        from log_collector.schema import DjangoExceptionSchema

        fn_data = f"{row}"
        payload = row["payload"]
        save = True

        try:
            payload = DjangoExceptionSchema(**payload).dict()
        except Exception as error:
            if PROD:
                exc_info = traceback.format_exception(error)
                exc_info = "\n".join(exc_info)
                collector_exception = CollectorException()
                collector_exception.fn_name = sprint("schema error", s=1)
                collector_exception.fn_data = fn_data
                collector_exception.exc_info = exc_info
                collector_exception.save()
                save = False

            if ALERTS:
                __upserver__.any_throw(
                    {"error": sprint(error, s=1)}, routing_key="alerts"
                )

            if DEBUG:
                sprint(error, c="red", p=1)
                raise Exception("DjangoException schema error")

        if save:
            record_check = DjangoException.objects.filter(
                exc_hash=payload["exc_hash"]
            ).first()
            if record_check:
                record_check.errors_count += 1
                record_check.save()

                if record_check.errors_count % 50 == 0 and ALERTS:
                    __upserver__.any_throw(
                        model_to_dict(record_check), routing_key="alerts"
                    )

            else:
                record = DjangoException()
                for field in cls._meta.fields:
                    field_name = field.name
                    if field_name in payload and payload[field_name]:
                        setattr(record, field_name, payload[field_name])
                try:
                    record.save()

                    if ALERTS:
                        __upserver__.any_throw(
                            model_to_dict(record), routing_key="alerts"
                        )

                    if DEBUG:
                        sprint("Record save [OK]", c="green", p=1)

                except Exception as error:
                    if PROD:
                        exc_info = traceback.format_exception(error)
                        exc_info = "\n".join(exc_info)
                        collector_exception = CollectorException()
                        collector_exception.fn_name = sprint("model save error", s=1)
                        collector_exception.fn_data = fn_data
                        collector_exception.exc_info = exc_info
                        collector_exception.save()

                    if ALERTS:
                        __upserver__.any_throw(
                            {"error": sprint(error, s=1)}, routing_key="alerts"
                        )

                    if DEBUG:
                        sprint(error, c="red", p=1)
                        raise Exception("DjangoException save error")

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % LOG_SIZE == 0):
            DjangoException.objects.all().delete()


post_save.connect(DjangoException.check_stat_size, sender=DjangoException)


class CollectorException(models.Model):
    fn_name = models.CharField(max_length=255)
    fn_data = models.TextField(null=True, blank=True)
    exc_info = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Self Collector Errors")
        verbose_name_plural = _("Self Collector Errors")

    def __str__(self):
        return f"{self.fn_name}"

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % LOG_SIZE == 0):
            CollectorException.objects.all().delete()


post_save.connect(CollectorException.check_stat_size, sender=CollectorException)


class TaskScheduler(models.Model):
    task_name = models.CharField(max_length=500)
    task_active = models.BooleanField(default=False)
    task_completed = models.BooleanField(default=False)
    task_time = models.FloatField(null=True, blank=True)
    task_stdout = models.TextField(null=True, blank=True)
    task_error_tb = models.TextField(null=True, blank=True)
    task_cron_time = models.CharField(max_length=100, null=True, blank=True)
    task_memory = models.TextField(null=True, blank=True)
    task_query_count = models.IntegerField(null=True, blank=True)
    task_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Task Scheduler")
        verbose_name_plural = _("Task Scheduler")

    def __str__(self):
        return f"{self.task_name}"

    @classmethod
    def check_stat_size(cls, sender, instance, created, *args, **kwargs):
        if created and (instance.id % 10000 == 0):
            TaskScheduler.objects.all().delete()


post_save.connect(TaskScheduler.check_stat_size, sender=TaskScheduler)
