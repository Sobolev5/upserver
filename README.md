# Upserver 

`upserver` it is a free monitoring tool with **repair** option.  
You can specify the ip of your server, login and password.  
If your server is unavailable, `upserver` will connect automatically and execute restore commands.
  
![](https://github.com/Sobolev5/upserver/blob/master/interface/static/upserver.png)

Example of use:  
- server monitoring    
- uptime statistic    
- server down alerting (in development)    

   
## Install and run
Clone repository first:   
```sh
git clone https://github.com/Sobolev5/upserver
mv .env.example .env
```

Change variables in *.env* file:
```sh
# ADMIN USER [CHANGE PASSWORD]
ADMIN_USER=admin
ADMIN_PASSWORD=password

# COMMON DB [CHANGE PASSWORD]
POSTGRES_DB=upserver_db
POSTGRES_USER=upserver_db_user
POSTGRES_PASSWORD=upserver_db_password
POSTGRES_HOST=upserver-postgres
POSTGRES_PORT=5432

# INTERFACE [CHANGE SECRET KEY]
SECRET_KEY=django-insecure-@x5%xegdelq=s!fybiup=pktful_+!t%x42y1!hh_=-p7$kz9s 
DEBUG=0

# LOGGER DB [CHANGE PASSWORD]
CLICKHOUSE_HOST=upserver-clickhouse
CLICKHOUSE_PORT=9000
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=default

# BROKER [CHANGE PASSWORD] 
RABBITMQ_HOST=upserver-rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=admin 
RABBITMQ_PASSWORD=admin
```

Start `upserver`:
```sh
docker-compose up --build -d
```

Run initial script:
```sh
docker exec upserver-interface sh /app/initial_database.sh
```

Open UI:  
```sh
http://YOU_SERVER_IP:12345 # Here you can log in with ADMIN_USER and ADMIN_PASSWORD
http://YOU_SERVER_IP:12345/monitoring/monitor/ # Monitors
http://YOU_SERVER_IP:12345/monitoring/monitoractivity/ # Monitors activity
http://YOU_SERVER_IP:12345/monitoring/restoreactivity/ # Restore activity (if monitor can not connect, we try to up remote service)
```

## Useful commands

Watch interface console:
```sh
docker logs upserver-interface --tail 100 --follow
```

Watch monitoring script console:
```sh
docker logs upserver-source --tail 100 --follow
```

Watch dependencies script console:
```sh
docker logs upserver-postgres --tail 100 --follow
docker logs upserver-clickhouse --tail 100 --follow
docker logs upserver-rabbitmq --tail 100 --follow
```

Migrate database (after pulling `upserver` updates):
```sh
docker exec upserver-interface python /app/manage.py migrate
```

Start `upserver`:
```sh
docker-compose up --build -d
```

Stop `upserver`:
```sh
docker-compose down
```

Backup database:
```sh
docker-compose exec -T upserver-postgres sh -c 'pg_dump -cU upserver_db_user upserver_db' > upserver.sql
```

Restore from backup:
```sh
cat upserver.sql | docker exec -i upserver-postgres psql -U upserver_db_user -d upserver_db
```

# Integrations
Upserver integrated with `django-clickhouse-logger` and `simple-print` from the box:
https://github.com/Sobolev5/django-clickhouse-logger (catch logs from Clickhouse)   
https://github.com/Sobolev5/simple-print (catch logs from RabbitMQ)   


First switch *.env* variables in your `upserver` local copy: 
``` sh  
CLICKHOUSE_LOGGER_ENABLED=1
SIMPLE_PRINT_ENABLED=1
```  

Second make install: 
``` sh
pip install simple-print
pip install django-clickhouse-logger 
```  

And put this variables in your *settings.py* file:
``` sh
DJANGO_CLICKHOUSE_LOGGER_HOST = "YOU_SERVER_IP"
DJANGO_CLICKHOUSE_LOGGER_PORT = 59000 # NOTE 59000 is Clickhouse port for Upserver
DJANGO_CLICKHOUSE_LOGGER_USER = "default"
DJANGO_CLICKHOUSE_LOGGER_PASSWORD = "default"
DJANGO_CLICKHOUSE_LOGGER_TTL_DAY = 3
DJANGO_CLICKHOUSE_LOGGER_REQUEST_EXTRA = "session"
SIMPLE_PRINT_AMQP_URI = "amqp://admin:admin@YOU_SERVER_IP:55672/vhost" # NOTE 55672 is RabbitMQ port for Upserver
```

Example of use (client side):
``` sh
from django_clickhouse_logger import capture_exception   
try:
    print(some_undefined_var)
except Exception as e:
    capture_exception(e)

from simple_print import throw
if log_condition == True:
    throw({"tag":"my tag", "msg":{"hello":"world"}}, uri=SIMPLE_PRINT_AMQP_URI) 
```

Userful integrations commands:
```sh
docker exec -it upserver-interface python /app/run.py integrations.tasks "get_clickhouse_logger_records()" # pull records for logger (django-clickhouse-logger)
docker exec -it upserver-interface python /app/run.py integrations.tasks "get_clickhouse_captured_exceptions()" # pull records for capture_exception (django-clickhouse-logger)
docker exec -it upserver-interface python /app/run.py integrations.tasks "catch_simple_print_messages()" # catch simple print messages (simple-print)
```

You can add this commands to cron (run every minute):
```sh
echo '* * * * * docker exec -i upserver-interface python /app/run.py integrations.tasks "get_clickhouse_logger_records()" &>/dev/null' >> /var/spool/cron/root 
echo '* * * * * docker exec -i upserver-interface python /app/run.py integrations.tasks "get_clickhouse_captured_exceptions()" &>/dev/null' >> /var/spool/cron/root 
echo '* * * * * docker exec -i upserver-interface python /app/run.py integrations.tasks "catch_simple_print_messages()" &>/dev/null' >> /var/spool/cron/root 
```

If you want to add your own integration, you can easy make a fork.




# TODO 
> api  
> server down alerts  
> tests  


# Time tracker for developers
Use [Workhours.space](https://workhours.space/) for your working time tracking. It is free.