from django.contrib import admin

from monitoring.models import Monitor
from monitoring.models import MonitorActivity
from monitoring.models import RestoreActivity


def enable(modeladmin, request, queryset):
    for object in queryset:
        object.active = True
        object.save()
enable.short_description = "Enable"


def disable(modeladmin, request, queryset):
    for object in queryset:
        object.active = False
        object.save()
disable.short_description = "Disable"


class MonitorAdmin(admin.ModelAdmin):
    raw_id_fields = [
        "user",
    ]
    list_display = [f.name for f in Monitor._meta.fields]
    list_editable = ["name", "host", "port", "su_host", "su_port", "su_login", "su_password", "su_restore_commands", "active"]
    actions = [enable, disable]
    save_as = True
admin.site.register(Monitor, MonitorAdmin)


class MonitorActivityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MonitorActivity._meta.fields] + ["restore_hops"]
    list_filter = ("monitor__name",)
admin.site.register(MonitorActivity, MonitorActivityAdmin)


class RestoreActivityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in RestoreActivity._meta.fields]
    list_filter = ("monitor__name", "exit_status")
admin.site.register(RestoreActivity, RestoreActivityAdmin)
