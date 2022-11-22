from django.db import models
from django.db.models.signals import post_save
from settings import LOG_SIZE


class SimplePrintCatch(models.Model):

    message = models.JSONField()
    tag = models.CharField(max_length=255)
    queue = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message}"

    @classmethod
    def check_stat_size(
        cls,
        sender,
        instance,
        created,
        *args,
        **kwargs
    ):
        if created and (instance.id % LOG_SIZE == 0):
            SimplePrintCatch.objects.all().delete()

post_save.connect(SimplePrintCatch.check_stat_size, sender=SimplePrintCatch)

