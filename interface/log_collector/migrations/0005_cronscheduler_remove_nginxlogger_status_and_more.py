# Generated by Django 4.1.7 on 2023-05-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("log_collector", "0004_alter_djangoexception_exc_info_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CronScheduler",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_name", models.CharField(max_length=255)),
                ("messages_count", models.TextField(blank=True, null=True)),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="nginxlogger",
            name="status",
        ),
        migrations.AddField(
            model_name="nginxlogger",
            name="status_code",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="body_bytes_sent",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="host",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="remote_addr",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="request_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="request_length",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="request_time",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="request_timestamp",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="request_uri",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="nginxlogger",
            name="server_addr",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
