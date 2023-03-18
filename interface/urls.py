from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
] 

admin.site.site_header = "Sys Collector"
admin.site.site_title = "Sys Collector"
admin.site.index_title = "Sys Collector"