# Upserver 

`upserver` it is a free monitoring tool with **repair** option.  
You can specify the ip of your server, login and password.  
If your server is unavailable, `upserver` will connect automatically and execute restore commands.
  
![](https://github.com/Sobolev5/upserver/blob/master/interface/static/upserver.png)

Example of use:  
- server monitoring    
- uptime statistic  
- env secrets (in development) 
- log collectors (in development) 
- server down alerting (in development)    

   
## Install and run
Clone repository first:   
```sh
git clone https://github.com/Sobolev5/upserver
mv .env.example .env
```

Change variables in *.env* file:
```sh
# ADMIN USER 
ADMIN_USER=admin
ADMIN_PASSWORD=admin

# INTERFACE [CHANGE SECRET KEY]
SECRET_KEY=django-insecure-@x5%xegdelq=s!fybiup=pktful_+!t%x42y1!hh_=-p71kz9s 
DEBUG=0

# DATABASE 
POSTGRES_HOST=upserver-postgres
POSTGRES_PORT=5432
POSTGRES_DB=db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin

# RABBITMQ
RABBITMQ_HOST=upserver-rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=admin 
RABBITMQ_PASSWORD=admin

# ALERTS
ALERTS=1
TELEGRAM_BOT_TOKEN=telegram_bot_token
TELEGRAM_CHAT_IDS=chat_id_1, chat_id_2  # For get your own chat ID use https://t.me/myidbot
```

Start `upserver`:
```sh
docker compose -f docker-compose.yml up --build -d
```

Run initial script (Required!):
```sh
docker exec upserver-interface python manage.py migrate
docker exec upserver-interface python run.py db_tasks "initial()"
```

Add cron scheduler:
```sh
echo '* * * * * docker exec -i upserver-interface python /interface/run.py log_collector.tasks "run_every_minute()" &>/dev/null' >> /var/spool/cron/root 
echo '* * * * * docker exec -i upserver-alerts python /alerts/run.py &>/dev/null' >> /var/spool/cron/root 
```

Open UI:  
```sh
http://YOU_SERVER_IP:12345 # Here you can log in with ADMIN_USER and ADMIN_PASSWORD
```

## Useful commands

Start/stop `upserver`:
```sh
docker compose -f docker-compose.yml up --build -d
docker compose down
```

Start/stop `upserver` dev mode (with `docker-compose.override.yml`): 
```sh
docker compose up --build -d
docker compose down
```

Get shell:
```sh
docker exec -it upserver-interface bash
```

Clear logs:
```sh
docker exec upserver-interface python run.py db_tasks "clear_logs()"
```

Watch consoles:
```sh
docker logs upserver-postgres --tail 100 --follow
docker logs upserver-rabbitmq --tail 100 --follow
docker logs upserver-interface --tail 100 --follow
docker logs upserver-alerts --tail 100 --follow
docker logs upserver-monitoring --tail 100 --follow
```

Migrate database (after pulling `upserver` updates):
```sh
docker exec upserver-interface python /interface/manage.py migrate
```

Backup database:
```sh
docker compose exec -T upserver-postgres sh -c 'pg_dump -cU admin db' > upserver.sql
```

Restore from backup:
```sh
cat upserver.sql | docker exec -i upserver-postgres psql -U admin -d db
```

Clear all:
```sh
docker compose down
docker system prune -a
```

Reinstall all:
```sh
docker compose down
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
docker compose -f docker-compose.yml up --build -d
docker exec upserver-interface python manage.py migrate
docker exec upserver-interface python run.py db_tasks "initial()"
```

# Log collectors
Upserver log collectors integrated with `throw-catch` from the box:
https://github.com/Sobolev5/throw-catch 
So you can easy write your own collector through RabbitMQ queues.

See `log_collectors` folder for examples.

