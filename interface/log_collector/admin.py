from django.contrib import admin
from django.db import models
from log_collector.models import DjangoLogger, DjangoException, \
                                 AnyLogger, NginxLogger, \
                                 CollectorException, CronScheduler  


class AnyLoggerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AnyLogger._meta.fields]
    list_filter = ("assigned_to", "filename", "function_name", "tag")
    list_editable = ("assigned_to",)
    search_fields = [f.name for f in AnyLogger._meta.fields if not isinstance(f, models.ForeignKey)]
admin.site.register(AnyLogger, AnyLoggerAdmin)


class DjangoLoggerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DjangoLogger._meta.fields]
    list_filter = ("assigned_to", "status", "user", "request_extra")
    list_editable = ("assigned_to", "status")
    search_fields = [f.name for f in DjangoLogger._meta.fields if not isinstance(f, models.ForeignKey)]
admin.site.register(DjangoLogger, DjangoLoggerAdmin)


class DjangoExceptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DjangoException._meta.fields]
    list_filter = ("assigned_to", "status", "exc_hash")
    list_editable = ("assigned_to",)
    search_fields = [f.name for f in DjangoException._meta.fields if not isinstance(f, models.ForeignKey)]
admin.site.register(DjangoException, DjangoExceptionAdmin)


class NginxLoggerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in NginxLogger._meta.fields]
    search_fields = [f.name for f in NginxLogger._meta.fields if not isinstance(f, models.ForeignKey)]
admin.site.register(NginxLogger, NginxLoggerAdmin)


class CollectorExceptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CollectorException._meta.fields]
    search_fields = [f.name for f in CollectorException._meta.fields if not isinstance(f, models.ForeignKey)]
admin.site.register(CollectorException, CollectorExceptionAdmin)


class CronSchedulerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CronScheduler._meta.fields]
    search_fields = [f.name for f in CronScheduler._meta.fields if not isinstance(f, models.ForeignKey)]
admin.site.register(CronScheduler, CronSchedulerAdmin)