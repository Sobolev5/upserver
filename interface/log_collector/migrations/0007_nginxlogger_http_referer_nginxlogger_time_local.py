# Generated by Django 4.1.7 on 2023-07-11 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_collector', '0006_rename_status_code_nginxlogger_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nginxlogger',
            name='http_referer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='nginxlogger',
            name='time_local',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
