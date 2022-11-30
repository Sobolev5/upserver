# Upserver 

`upserver` it is a free monitoring tool with **repair** option.  
You can specify the ip of your server, login and password.  
If your server is unavailable, `upserver` will connect automatically and execute restore commands.
  
Example of use:  
- server monitoring    
- uptime statistic    
- server down alerting (in development)    

   
## Install and run
Clone repository first:   
```sh
git clone https://github.com/Sobolev5/upserver
```

Rename .env.example to .env and change ENV variables:
```sh
# ADMIN USER [CHANGE ALL]
ADMIN_USER=admin
ADMIN_PASSWORD=password

# DATABASE [CHANGE IF NECESSARY, NOT REQUIRED]
POSTGRES_DB=upserver_db
POSTGRES_USER=upserver_db_user
POSTGRES_PASSWORD=upserver_db_password
POSTGRES_HOST=upserver-postgres
POSTGRES_PORT=5432

# INTERFACE [CHANGE SECRET KEY]
SECRET_KEY=django-insecure-@x5%xegdelq=s!fybiup=pktful_+!t%x42y1!hh_=-p7$kz9s 
DEBUG=0
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
Upserver integrated with `simple-print` and `django-clickhouse-logger` from the box:
https://github.com/Sobolev5/simple-print (catch logs from RabbitMQ)
https://github.com/Sobolev5/django-clickhouse-logger (catch logs from Clickhouse)  
  
If you want to add your own integration, you can easy make a fork.


# TODO 
> api  
> server down alerting  
> tests  
