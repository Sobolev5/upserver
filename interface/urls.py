from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
] 

admin.site.site_header = "Upserver"
admin.site.site_title = "Upserver"
admin.site.index_title = "Upserver"