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
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('port', models.PositiveIntegerField()),
                ('su_host', models.CharField(blank=True, max_length=255, null=True)),
                ('su_port', models.PositiveIntegerField(default=22)),
                ('su_login', models.CharField(blank=True, max_length=255, null=True)),
                ('su_password', models.CharField(blank=True, max_length=255, null=True)),
                ('su_restore_commands', models.TextField(blank=True, null=True)),
                ('restore_hops', models.PositiveIntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RestoreActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('console_log', models.TextField(blank=True, null=True)),
                ('exit_status', models.CharField(blank=True, max_length=255, null=True)),
                ('creation_date', models.CharField(blank=True, max_length=255, null=True)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.monitor')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='MonitorActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_response', models.CharField(blank=True, max_length=255, null=True)),
                ('server_available', models.BooleanField(default=True)),
                ('creation_date', models.CharField(blank=True, max_length=255, null=True)),
                ('monitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.monitor')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]