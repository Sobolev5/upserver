# Development commands

Run commands `upserver.interface`: 
```sh
docker exec upserver-interface python /interface/run.py db_tasks "clear_all()"
docker exec upserver-interface python /interface/run.py db_tasks "clear_logs()"
docker exec upserver-interface python /interface/run.py db_tasks "prepare()"
docker exec upserver-interface python manage.py makemigrations
docker exec upserver-interface python manage.py migrate
docker exec upserver-interface python /interface/run.py log_collector.tasks "run_every_minute()"
docker exec upserver-interface pytest
```

Run commands `upserver.alerts`: 
```sh
docker exec upserver-alerts python /alerts/run.py 
``` 

Get logs:
```sh
docker compose logs -f upserver-interface 
docker compose logs -f upserver-alerts
docker compose logs -f upserver-interface upserver-alerts
docker compose logs -f upserver-monitoring
``` 

Start/stop `upserver` in dev mode: 
```sh
docker compose up
```

Start/stop `upserver` in production mode: 
```sh
docker compose up --build -d
docker compose down
```

 