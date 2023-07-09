import traceback
from logger import logger
from simple_print import sprint
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from settings import LOG_SIZE
from settings import ALERTS
from settings import DEBUG
from settings import TEST
from settings import PROD
from django.forms.models import model_to_dict
from log_collector.utils import parse_nginx_log
import __upserver__


class AnyLogger(models.Model):
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) 
    payload = models.JSONField()
    tag = models.CharField(max_length=255)
    routing_key = models.CharField(max_length=255)
    ttl = models.PositiveIntegerField(default=1) 
    filename = models.CharField(max_length=255, null=True, blank=True)  
    function_name = models.CharField(max_length=255, null=True, blank=True)  
    lineno = models.PositiveIntegerField(default=1) 
    send_datetime = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)

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

            if DEBUG:
                sprint(error, c="red", p=1)

            if TEST:
                raise Exception("AnyLogger schema error")
            
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
                __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts") 

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
                    sprint("OK", c="green", p=1)

                if TEST:
                    logger.info("OK")

            except Exception as error:

                if DEBUG:
                    sprint(error, c="red", p=1)
                
                if TEST:
                    raise Exception("AnyLogger save error")               

                if PROD:
                    exc_info = traceback.format_exception(error)
                    exc_info = "\n".join(exc_info)
                    collector_exception = CollectorException() 
                    collector_exception.fn_name = sprint("model save error", s=1)
                    collector_exception.fn_data = fn_data
                    collector_exception.exc_info = exc_info
                    collector_exception.save()   

                if ALERTS:
                    __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts")

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
            AnyLogger.objects.all().delete()

post_save.connect(AnyLogger.check_stat_size, sender=AnyLogger)


class DjangoLogger(models.Model):

    class StatusChoices(models.TextChoices):
        NEW = 'new', _('New')
        IN_PROCCESS = 'in_proccess', _('In proccess')
        RESOLVED = 'resolved', _('Resolved')
        NOT_RESOLVED = 'not_resolved', _('Not resolved')

    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=24, choices=StatusChoices.choices, default=StatusChoices.NEW)
    errors_count = models.PositiveIntegerField(default=0)
    asctime = models.DateTimeField(auto_now_add=True)    
    exc_info = models.TextField(null=True, blank=True)
    exc_hash = models.CharField(max_length=255, unique=True)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    user = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.PositiveIntegerField(default=22, null=True, blank=True)
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
    creation_date = models.DateTimeField(auto_now_add=True)

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

            if DEBUG:
                sprint(error, c="red", p=1)    

            if TEST:
                raise Exception("DjangoLogger schema error")                

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
                __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts")    

        if save:
            record_check = DjangoLogger.objects.filter(exc_hash=payload["exc_hash"]).first()
            if record_check:
                record_check.errors_count += 1
                record_check.save()

                if record_check.errors_count % 50 == 0 and ALERTS:
                    __upserver__.any_throw(model_to_dict(record_check), routing_key="alerts")

            else:
                record = DjangoLogger()
                for field in cls._meta.fields:             
                    field_name = field.name
                    if field_name in payload and payload[field_name]:         
                        setattr(record, field_name, payload[field_name]) 
                try:
                    record.save()

                    if ALERTS:
                        __upserver__.any_throw(model_to_dict(record), routing_key="alerts")

                    if TEST:
                        logger.info("OK")

                    if DEBUG:
                        sprint("OK", c="green", p=1)

                except Exception as error:

                    if DEBUG:
                        sprint(error, c="red", p=1)                   

                    if TEST:
                        raise Exception("DjangoLogger save error")
                    
                    if PROD:
                        exc_info = traceback.format_exception(error)
                        exc_info = "\n".join(exc_info)
                        collector_exception = CollectorException()                    
                        collector_exception.fn_name = sprint("model save error", s=1)
                        collector_exception.fn_data = fn_data
                        collector_exception.exc_info = exc_info
                        collector_exception.save()   

                    if ALERTS:
                        __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts")                         

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
            DjangoLogger.objects.all().delete()

post_save.connect(DjangoLogger.check_stat_size, sender=DjangoLogger)


class DjangoException(models.Model):

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
    message = models.CharField(max_length=5000, null=True, blank=True) 
    creation_date = models.DateTimeField(auto_now_add=True)

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

            if DEBUG:
                sprint(error, c="red", p=1)    

            if TEST:
                raise Exception("DjangoException schema error")    
            
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
                __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts") 

        if save:
            record_check = DjangoException.objects.filter(exc_hash=payload["exc_hash"]).first()
            if record_check:
                record_check.errors_count += 1
                record_check.save()

                if record_check.errors_count % 50 == 0 and ALERTS:
                    __upserver__.any_throw(model_to_dict(record_check), routing_key="alerts")

            else:

                record = DjangoException()
                for field in cls._meta.fields:             
                    field_name = field.name
                    if field_name in payload and payload[field_name]:         
                        setattr(record, field_name, payload[field_name]) 
                try:
                    record.save()

                    if ALERTS:
                        __upserver__.any_throw(model_to_dict(record), routing_key="alerts")

                    if DEBUG:
                        sprint("OK", c="green", p=1)  

                    if TEST:
                        logger.info("OK")

                except Exception as error:

                    if DEBUG:
                        sprint(error, c="red", p=1)      

                    if TEST:
                        raise Exception("DjangoException save error") 

                    if PROD:       
                        exc_info = traceback.format_exception(error)
                        exc_info = "\n".join(exc_info)
                        collector_exception = CollectorException()                    
                        collector_exception.fn_name = sprint("model save error", s=1)
                        collector_exception.fn_data = fn_data
                        collector_exception.exc_info = exc_info
                        collector_exception.save()   

                    if ALERTS:
                        __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts")

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
            DjangoException.objects.all().delete()

post_save.connect(DjangoException.check_stat_size, sender=DjangoException)


class NginxLogger(models.Model):

    class Scheme(models.TextChoices):
        UNKNOWN = 'unknown', 'unknown'
        HTTP = 'http', 'http'
        HTTPS = 'https', 'https'

    class RequestMethod(models.TextChoices):
        UNKNOWN = "UNKNOWN", "UNKNOWN" 
        OPTIONS = "OPTIONS", "OPTIONS"
        GET = "GET", "GET"
        HEAD = "HEAD", "HEAD"
        POST = "POST", "POST"
        PATCH = "PATCH", "PATCH"
        PUT = "PUT", "PUT"
        DELETE = "DELETE", "DELETE"
    
    request_id = models.CharField(max_length=255, null=True, blank=True)
    request_timestamp = models.DateTimeField(null=True, blank=True)
    remote_user = models.CharField(max_length=255, null=True, blank=True)
    remote_addr = models.CharField(max_length=255, null=True, blank=True)
    scheme = models.CharField(max_length=24, choices=Scheme.choices, default=Scheme.UNKNOWN)
    host = models.CharField(max_length=255, null=True, blank=True)
    server_addr = models.CharField(max_length=255, null=True, blank=True)
    request_method = models.CharField(max_length=24, choices=RequestMethod.choices, default=RequestMethod.UNKNOWN)
    request_uri = models.CharField(max_length=255, null=True, blank=True)
    request_length = models.PositiveIntegerField(null=True)
    request_time = models.FloatField(null=True)
    status_code = models.PositiveIntegerField(null=True)
    body_bytes_sent = models.PositiveIntegerField(null=True)
    upstream_addr = models.CharField(max_length=255, null=True, blank=True)
    upstream_connect_time = models.FloatField(null=True)
    upstream_header_time = models.FloatField(null=True)
    upstream_response_time = models.FloatField(null=True)
    http_referrer = models.CharField(max_length=255, null=True)
    http_user_agent = models.CharField(max_length=255, null=True)
    http_x_forwarded_for = models.CharField(max_length=255, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_id}"

    @classmethod
    def save_records(cls, f_binary):    
        try:
            rows = []
            records_count = 0
            for counter, line in enumerate(parse_nginx_log(f_binary)):
                rows.append(line)
                if counter % 100 == 0:

                    if DEBUG:
                        sprint("100 OK", c="green", p=1)   
                    
                    NginxLogger.objects.bulk_create([NginxLogger(**row) for row in rows])
                    rows = []
                records_count += 1

            # write last
            NginxLogger.objects.bulk_create([NginxLogger(**row) for row in rows])

            if TEST:
                logger.info("OK")

            if DEBUG:
                sprint("OK", c="green", p=1)

            if ALERTS:
                __upserver__.any_throw({"success": f"Nginx parsed [ OK ] Records created {records_count}"}, routing_key="alerts")                

        except Exception as error:

            if DEBUG:
                sprint(error, c="red", p=1)                   

            if TEST:
                raise Exception("NginxLogger error")
            
            if PROD:
                exc_info = traceback.format_exception(error)
                exc_info = "\n".join(exc_info)
                collector_exception = CollectorException()                    
                collector_exception.fn_name = sprint("model save error", s=1)
                collector_exception.fn_data = "nginx_file"
                collector_exception.exc_info = exc_info
                collector_exception.save()   

            if ALERTS:
                __upserver__.any_throw({"error": sprint(error, s=1)}, routing_key="alerts") 

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
            NginxLogger.objects.all().delete()

post_save.connect(NginxLogger.check_stat_size, sender=NginxLogger)


class CollectorException(models.Model):
    """ Collect Upserver exceptions in separate table. """
    fn_name = models.CharField(max_length=255) 
    fn_data = models.TextField(null=True, blank=True)
    exc_info = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fn_name}"

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
            CollectorException.objects.all().delete()

post_save.connect(CollectorException.check_stat_size, sender=CollectorException)


class CronScheduler(models.Model):
    task_name = models.CharField(max_length=255) 
    messages_count = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fn_name}"

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
            CollectorException.objects.all().delete()

post_save.connect(CronScheduler.check_stat_size, sender=CronScheduler)