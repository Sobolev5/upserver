from django.contrib import admin
from integrations.models import SimplePrintCatch

class MonitorActivityAdmin(admin.ModelAdmin):
    list_display = [f.name for f in MonitorActivity._meta.fields]
    list_filter = ("monitor__name",)
admin.site.register(MonitorActivity, MonitorActivityAdmin)