import settings
from django.contrib import admin
from django.db import models
from integrations.models import ClickHouseLogger, ClickHouseCaptureException, SimplePrintCatch


if settings.CLICKHOUSE_LOGGER_ENABLED:
    class ClickHouseLoggerAdmin(admin.ModelAdmin):
        list_display = [f.name for f in ClickHouseLogger._meta.fields]
        list_filter = ("assigned_to", "status", "user", "request_extra")
        search_fields = [f.name for f in ClickHouseLogger._meta.fields if not isinstance(f, models.ForeignKey)]
    admin.site.register(ClickHouseLogger, ClickHouseLoggerAdmin)

    class ClickHouseCaptureExceptionAdmin(admin.ModelAdmin):
        list_display = [f.name for f in ClickHouseCaptureException._meta.fields]
        list_filter = ("assigned_to", "status", "exc_hash")
        search_fields = [f.name for f in ClickHouseLogger._meta.fields if not isinstance(f, models.ForeignKey)]
    admin.site.register(ClickHouseCaptureException, ClickHouseCaptureExceptionAdmin)

if settings.SIMPLE_PRINT_ENABLED:
    class SimplePrintCatchAdmin(admin.ModelAdmin):
        list_display = [f.name for f in SimplePrintCatch._meta.fields]
        list_filter = ("assigned_to", "filename", "function_name", "tag")
        search_fields = [f.name for f in ClickHouseLogger._meta.fields if not isinstance(f, models.ForeignKey)]
    admin.site.register(SimplePrintCatch, SimplePrintCatchAdmin)