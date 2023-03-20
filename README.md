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
# ADMIN USER [CHANGE PASSWORD]
ADMIN_USER=admin
ADMIN_PASSWORD=password

# POSTGRES  [CHANGE PASSWORD]
POSTGRES_DB=upserver_db
POSTGRES_USER=upserver_db_user
POSTGRES_PASSWORD=upserver_db_password
POSTGRES_HOST=upserver-postgres
POSTGRES_PORT=5432

# RABBITMQ [CHANGE PASSWORD] 
RABBITMQ_USER=admin 
RABBITMQ_PASSWORD=admin
RABBITMQ_HOST=upserver-rabbitmq
RABBITMQ_PORT=5672


# INTERFACE [CHANGE SECRET KEY AND TELEGRAM BOT TOKEN]
SECRET_KEY=django-insecure-@x5%xegdelq=s!fybiup=pktful_+!t%x42y1!hh_=-p7$kz9s 
DEBUG=0
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_IDS=your_chat_id, another_admin_chat_id
```

Start `upserver`:
```sh
docker-compose up --build -d
```

Run initial script (Required):
```sh
docker exec upserver-interface python run.py db_tasks "initial()"
```

Add cron scheduler:
```sh
echo '* * * * * docker exec -i upserver-interface python /app/run.py log_collector.tasks "run_every_minute()" &>/dev/null' >> /var/spool/cron/root 
```

Open UI:  
```sh
http://YOU_SERVER_IP:12345 # Here you can log in with ADMIN_USER and ADMIN_PASSWORD
```

## Useful commands

Get shell:
```sh
docker exec -it upserver-interface sh
```

Clear logs:
```sh
docker exec upserver-interface python run.py db_tasks "clear_logs()"
```

Watch interface console:
```sh
docker logs upserver-interface --tail 100 --follow
```

Watch monitoring console:
```sh
docker logs upserver-source --tail 100 --follow
```

Watch dependencies console:
```sh
docker logs upserver-postgres --tail 100 --follow
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

# Log collectors
Upserver log collectors integrated with `throw-catch` from the box:
https://github.com/Sobolev5/throw-catch 
So you can easy write your own collector through RabbitMQ queues.

See `log_collectors` folder for examples.

