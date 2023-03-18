from django.apps import AppConfig


class LogCollectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'log_collector'
    verbose_name = 'Log Collector'