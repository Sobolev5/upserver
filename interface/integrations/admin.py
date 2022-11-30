from django.contrib import admin
from integrations.models import ClickHouseLogger, ClickHouseCaptureException, SimplePrintCatch


class ClickHouseLoggerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClickHouseLogger._meta.fields]
    list_filter = ("assigned_to", "exc_hash", "funcName")
admin.site.register(ClickHouseLogger, ClickHouseLoggerAdmin)


class ClickHouseCaptureExceptionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ClickHouseCaptureException._meta.fields]
    list_filter = ("assigned_to", "exc_hash")
admin.site.register(ClickHouseCaptureException, ClickHouseCaptureExceptionAdmin)


class SimplePrintCatchAdmin(admin.ModelAdmin):
    list_display = [f.name for f in SimplePrintCatch._meta.fields]
    list_filter = ("assigned_to", "tag", "queue")
admin.site.register(SimplePrintCatch, SimplePrintCatchAdmin)