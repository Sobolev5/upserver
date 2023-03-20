import datetime
import traceback
import pprint
from functools import wraps
from croniter import croniter
from throw_catch import catch
from settings import AMQP_URI
from log_collector import schema
from log_collector import models


class Tasks:

    def apply_cron_like_time(cron_time):
        """
        apply fn.cron_time
        """
        def decorator(fn):
            @wraps(fn)
            def wrapper(*a, **kw):
                return fn(*a, **kw)
            wrapper.cron_time = cron_time
            return wrapper
        return decorator

    @apply_cron_like_time("* * * * *")
    def catch_any_logger():
        for row in catch(uri=AMQP_URI, queue="any_logger", count=1):
            models.AnyLogger.save_record(row=row)

    @apply_cron_like_time("* * * * *")
    def catch_django_logger():
        for row in catch(uri=AMQP_URI, queue="django_logger", count=1):
            models.DjangoLogger.save_record(row=row)

    @apply_cron_like_time("* * * * *")
    def catch_django_exception():
        for row in catch(uri=AMQP_URI, queue="django_exception", count=1):
            models.DjangoException.save_record(row=row)

    # @apply_cron_like_time("* * * * *")
    # def catch_nginx_logger():
    #     for message in catch(uri=AMQP_URI, queue="nginx_logger", count=50):
    #         obj = schema.NginxLogger(**message)
    #         print(obj)
    #         print(type(obj))


def run_every_minute():
    # python run.py log_collector.tasks "run_every_minute()"
    datetime_now = datetime.datetime.now()
    for fn_name, fn in filter(lambda x: x[0].startswith("catch"), Tasks.__dict__.items()):
        cron_time = None
        if hasattr(fn, "cron_time") and fn.cron_time:
            cron_time = fn.cron_time

        if cron_time and croniter.match(cron_time, datetime_now):
            try:
                fn()
            except Exception as error:
                exc_info = traceback.format_exception(error)
                exc_info = "\n".join(exc_info)
                collector_exception = models.CollectorException() 
                collector_exception.fn_name = fn_name
                collector_exception.exc_info = exc_info
                collector_exception.save()


