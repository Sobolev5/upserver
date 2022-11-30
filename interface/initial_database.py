import os
from django.contrib.auth.models import User
from simple_print import sprint
from monitoring.models import Monitor


def clear() -> None:
    # python run.py initial_data "clear_database()"
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    Monitor.objects.all().delete()
    sprint("Clear_database -> complete", c="green")


def prepare() -> None:
    # python run.py initial_data "prepare()"
    username = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD")
    superuser = User.objects.create_superuser(username=username, email=f"{username}@upserver.dot", password=password)
    superuser.save()

    monitors_list = [
        {"name": "workhours",
         "host": "workhours.space",
         "port": 443,
         "su_host": "workhours.space",
         "su_port": 22,
         "su_login": "root",
         "su_password": "mypass",
         "su_restore_commands": "cd /var/www/workhours; docker-compose down; docker-compose up --build -d",
         "active": True
        },
        {"name": "0xDating",
         "host": "0xdating.space",
         "port": 443,
         "su_host": "0xdating.space",
         "su_port": 22,
         "su_login": "root",
         "su_password": "mypass",
         "su_restore_commands": "cd /var/www/dating; docker-compose down; docker-compose up --build -d",
         "active": True
        }
    ]
    for monitor_dict in monitors_list:

        monitor = Monitor()
        monitor.user = superuser
        for k, v in monitor_dict.items():
            monitor.__setattr__(k, v)
        monitor.save()
        sprint(f"monitor successfully created ID={monitor.id}")

    sprint("Fill_database -> complete", c="green")