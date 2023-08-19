import os
from django.contrib.auth.models import User
from simple_print import sprint
from log_collector.models import DjangoLogger
from log_collector.models import DjangoException
from log_collector.models import AnyLogger
from log_collector.models import NginxLogger
from log_collector.models import CollectorException
from log_collector.models import TaskScheduler
from monitoring.models import Monitor
from monitoring.models import MonitorActivity
from monitoring.models import RestoreActivity
from mixer.backend.django import mixer


def clear_all() -> None:
    # python run.py db_tasks "clear_all()"

    User.objects.all().delete()
    DjangoLogger.objects.all().delete()
    DjangoException.objects.all().delete()
    AnyLogger.objects.all().delete()
    NginxLogger.objects.all().delete()
    Monitor.objects.all().delete()
    sprint("db_tasks.clear_all -> complete", c="green")


def clear_logs() -> None:
    # python run.py db_tasks "clear_logs()"

    DjangoLogger.objects.all().delete()
    DjangoException.objects.all().delete()
    AnyLogger.objects.all().delete()
    NginxLogger.objects.all().delete()
    CollectorException.objects.all().delete()
    TaskScheduler.objects.all().delete()
    MonitorActivity.objects.all().delete()
    RestoreActivity.objects.all().delete()
    sprint("db_tasks.clear_logs -> complete", c="green")
    

def initial() -> None:
    # python run.py db_tasks "prepare()"

    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD") 

    su_email = f"{username}@up.server"
    initialized = True

    try:
       superuser = User.objects.get(email=su_email) 
    except:
        superuser = User.objects.create_superuser(username=username, email=su_email, password=password)
        superuser.save()
        initialized = False
    
    if not initialized:

        monitors_list = [
            {"name": "httpbin.org",
            "host": "httpbin.org",
            "port": 443,
            "su_host": "httpbin.org",
            "su_port": 22,
            "su_login": "root",
            "su_password": "mypass",
            "su_restore_commands": "cd /var/opt; ./restore",
            "active": True
            }
        ]

        for monitor_dict in monitors_list:
            monitor = Monitor()
            monitor.user = superuser
            for k, v in monitor_dict.items():
                monitor.__setattr__(k, v)
            monitor.save()
            sprint(f"Monitor successfully created ID={monitor.id}")

        for i in range(10):
            o = mixer.blend(DjangoLogger, assigned_to=superuser)
            o.save()

        for i in range(10):
            o = mixer.blend(DjangoException, assigned_to=superuser)
            o.save()

        for i in range(10):
            o = mixer.blend(NginxLogger)
            o.save()    

        sprint("db_tasks.initial -> complete", c="green")
    else:
        sprint("db_tasks.initial -> database already intialized", c="yellow")
