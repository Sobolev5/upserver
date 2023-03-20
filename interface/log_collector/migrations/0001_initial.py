# Generated by Django 4.1.1 on 2023-03-16 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectorException',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fn_name', models.CharField(max_length=255)),
                ('exc_info', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'CollectorException',
                'verbose_name_plural': 'CollectorException',
            },
        ),
        migrations.CreateModel(
            name='NginxLogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.CharField(max_length=255)),
                ('request_timestamp', models.DateTimeField()),
                ('remote_user', models.CharField(blank=True, max_length=255, null=True)),
                ('remote_addr', models.CharField(max_length=255)),
                ('scheme', models.CharField(choices=[('unknown', 'unknown'), ('http', 'http'), ('https', 'https')], default='unknown', max_length=24)),
                ('host', models.CharField(max_length=255)),
                ('server_addr', models.CharField(max_length=255)),
                ('request_method', models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('OPTIONS', 'OPTIONS'), ('GET', 'GET'), ('HEAD', 'HEAD'), ('POST', 'POST'), ('PATCH', 'PATCH'), ('PUT', 'PUT'), ('DELETE', 'DELETE')], default='UNKNOWN', max_length=24)),
                ('request_uri', models.CharField(max_length=255)),
                ('request_length', models.PositiveIntegerField()),
                ('request_time', models.FloatField()),
                ('status', models.PositiveIntegerField()),
                ('body_bytes_sent', models.PositiveIntegerField()),
                ('upstream_addr', models.CharField(blank=True, max_length=255, null=True)),
                ('upstream_connect_time', models.FloatField(null=True)),
                ('upstream_header_time', models.FloatField(null=True)),
                ('upstream_response_time', models.FloatField(null=True)),
                ('http_referrer', models.CharField(max_length=255, null=True)),
                ('http_user_agent', models.CharField(max_length=255, null=True)),
                ('http_x_forwarded_for', models.CharField(max_length=255, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'NginxLogger',
                'verbose_name_plural': 'NginxLogger',
            },
        ),
        migrations.CreateModel(
            name='DjangoLogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'New'), ('in_proccess', 'In proccess'), ('resolved', 'Resolved'), ('not_resolved', 'Not resolved')], default='new', max_length=24)),
                ('errors_count', models.PositiveIntegerField(default=0)),
                ('uuid', models.CharField(blank=True, max_length=255, null=True)),
                ('asctime', models.DateTimeField(auto_now_add=True)),
                ('exc_info', models.TextField(blank=True, null=True)),
                ('exc_hash', models.CharField(max_length=255, unique=True)),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('user_id', models.PositiveIntegerField(default=22)),
                ('request_extra', models.TextField(blank=True, null=True)),
                ('site', models.CharField(blank=True, max_length=255, null=True)),
                ('scheme', models.CharField(blank=True, max_length=255, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('method', models.CharField(blank=True, max_length=255, null=True)),
                ('GET', models.TextField(blank=True, null=True)),
                ('POST', models.TextField(blank=True, null=True)),
                ('headers', models.TextField(blank=True, null=True)),
                ('args', models.TextField(blank=True, null=True)),
                ('kwargs', models.TextField(blank=True, null=True)),
                ('pathname', models.CharField(blank=True, max_length=255, null=True)),
                ('funcName', models.CharField(blank=True, max_length=255, null=True)),
                ('lineno', models.PositiveIntegerField(default=1)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('exc_text', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.FloatField(blank=True, null=True)),
                ('filename', models.CharField(blank=True, max_length=255, null=True)),
                ('levelname', models.CharField(blank=True, max_length=255, null=True)),
                ('levelno', models.CharField(blank=True, max_length=255, null=True)),
                ('module', models.CharField(blank=True, max_length=255, null=True)),
                ('msecs', models.FloatField(default=22)),
                ('msg', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('process', models.CharField(blank=True, max_length=255, null=True)),
                ('processName', models.CharField(blank=True, max_length=255, null=True)),
                ('relativeCreated', models.CharField(blank=True, max_length=255, null=True)),
                ('stack_info', models.CharField(blank=True, max_length=255, null=True)),
                ('thread', models.CharField(blank=True, max_length=255, null=True)),
                ('threadName', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DjangoLogger',
                'verbose_name_plural': 'DjangoLogger',
            },
        ),
        migrations.CreateModel(
            name='DjangoException',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'New'), ('in_proccess', 'In proccess'), ('resolved', 'Resolved'), ('not_resolved', 'Not resolved')], default='new', max_length=24)),
                ('errors_count', models.PositiveIntegerField(default=0)),
                ('uuid', models.CharField(blank=True, max_length=255, null=True)),
                ('asctime', models.DateTimeField(auto_now_add=True)),
                ('exc_info', models.CharField(blank=True, max_length=255, null=True)),
                ('exc_hash', models.CharField(max_length=255, unique=True)),
                ('message', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DjangoException',
                'verbose_name_plural': 'DjangoException',
            },
        ),
        migrations.CreateModel(
            name='AnyLogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payload', models.JSONField()),
                ('tag', models.CharField(max_length=255)),
                ('routing_key', models.CharField(max_length=255)),
                ('ttl', models.PositiveIntegerField(default=1)),
                ('filename', models.CharField(blank=True, max_length=255, null=True)),
                ('function_name', models.CharField(blank=True, max_length=255, null=True)),
                ('lineno', models.PositiveIntegerField(default=1)),
                ('send_datetime', models.DateTimeField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'AnyLogger',
                'verbose_name_plural': 'AnyLogger',
            },
        ),
    ]