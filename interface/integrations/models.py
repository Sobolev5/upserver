from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from settings import LOG_SIZE


class ClickHouseLogger(models.Model):

    class StatusChoices(models.TextChoices):
        NEW = 'new', _('New')
        IN_PROCCESS = 'in_proccess', _('In proccess')
        RESOLVED = 'resolved', _('Resolved')
        NOT_RESOLVED = 'not_resolved', _('Not resolved')

    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=24, choices=StatusChoices.choices, default=StatusChoices.NEW)
    errors_count = models.PositiveIntegerField(default=0)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    asctime = models.DateTimeField(auto_now_add=True)    
    exc_info = models.TextField(null=True, blank=True)
    exc_hash = models.CharField(max_length=255, unique=True)
    user = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.PositiveIntegerField(default=22)
    request_extra = models.CharField(max_length=255, null=True, blank=True)
    site = models.CharField(max_length=255, null=True, blank=True)   
    scheme = models.CharField(max_length=255, null=True, blank=True)  
    body = models.CharField(max_length=255, null=True, blank=True)  
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
    module= models.CharField(max_length=255, null=True, blank=True)
    msecs = models.FloatField(default=22)
    msg = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    process = models.CharField(max_length=255, null=True, blank=True)
    processName = models.CharField(max_length=255, null=True, blank=True)
    relativeCreated = models.CharField(max_length=255, null=True, blank=True)
    stack_info = models.CharField(max_length=255, null=True, blank=True)
    thread = models.CharField(max_length=255, null=True, blank=True)  
    threadName = models.CharField(max_length=255, null=True, blank=True) 

    class Meta:
        verbose_name = 'Django Errors (django-clickhouse-logger)'
        verbose_name_plural = 'Django Errors (django-clickhouse-logger)'

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
            ClickHouseLogger.objects.all().delete()

post_save.connect(ClickHouseLogger.check_stat_size, sender=ClickHouseLogger)


class ClickHouseCaptureException(models.Model):

    class StatusChoices(models.TextChoices):
        NEW = 'new', _('New')
        IN_PROCCESS = 'in_proccess', _('In proccess')
        RESOLVED = 'resolved', _('Resolved')
        NOT_RESOLVED = 'not_resolved', _('Not resolved')

    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=24, choices=StatusChoices.choices, default=StatusChoices.NEW)
    errors_count = models.PositiveIntegerField(default=0)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    asctime = models.DateTimeField(auto_now_add=True)    
    exc_info = models.CharField(max_length=255, null=True, blank=True)
    exc_hash = models.CharField(max_length=255, unique=True)
    message = models.CharField(max_length=255, null=True, blank=True) 

    class Meta:
        verbose_name = 'Captured exceptions (django-clickhouse-logger)'
        verbose_name_plural = 'Captured exceptions (django-clickhouse-logger)'

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

post_save.connect(ClickHouseCaptureException.check_stat_size, sender=ClickHouseCaptureException)


class SimplePrintCatch(models.Model):
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) 
    tag = models.CharField(max_length=255)
    message = models.JSONField()
    uuid = models.CharField(max_length=255, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)  
    function_name = models.CharField(max_length=255, null=True, blank=True)  
    lineno = models.PositiveIntegerField(default=1) 
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Get alerts (simple-print)'
        verbose_name_plural = 'Get alerts (simple-print)'

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

