# upserver-django-logger

Logger configuration in settings.py:
```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue",}, 
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "formatters": {
        "console": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {"level": "INFO", "filters": ["require_debug_true"], "class": "logging.StreamHandler", "formatter": "console"},
        "django_logger": {"level": "ERROR", "filters": ["require_debug_false"], "class": "django_clickhouse_logger.handlers.LoggerHandler"},              
    }, 
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO",},
        "django.request": {"handlers": ["django_logger"], "level": "ERROR", 'propagate': False},
    },
}
```

If you want to test just change filter `require_debug_false` to `require_debug_true` 
for `django_logger` handler and raise error in any django view.  
  

# Capture exception
To catch exceptions manually:
```python

from django_logger import capture_exception   

try:
    print(undefined_variable)
except Exception as e:
    capture_exception(e)

try:
    print(undefined_variable)
except Exception as e:
    capture_exception(e, "add some text here")
```

# Collect logs on upserver side
For collect logs add this command to cron:
```sh
echo '* * * * * docker exec -i upserver-interface python /app/run.py log_collector.tasks "run_every_minute()" &>/dev/null' >> /var/spool/cron/root 
```

