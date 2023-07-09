# Development commands

Start/stop `upserver` in dev mode: 
```sh
docker compose -f docker-compose.yml -f docker-compose.dev.yml --profile all up --build -d
docker compose -f docker-compose.yml -f docker-compose.dev.yml --profile all down
```

Run tests: 
```sh
docker compose -f docker-compose.yml -f docker-compose.test.yml --profile app up 
```

Run commands `upserver.interface`: 
```sh
docker exec upserver-interface python /interface/run.py db_tasks "clear_all()"
docker exec upserver-interface python /interface/run.py db_tasks "clear_logs()"
docker exec upserver-interface python /interface/run.py db_tasks "clear_monitoring()"
docker exec upserver-interface python /interface/run.py db_tasks "prepare()"
docker exec upserver-interface python /interface/run.py log_collector.tasks "run_every_minute()"
docker exec upserver-interface pytest
```

Run commands `upserver.alerts`: 
```sh
docker exec upserver-alerts python /alerts/run.py 
``` 

Get logs:
```sh
docker compose logs -f upserver-interface upserver-alerts
docker compose logs -f upserver-monitoring
``` 

Start/stop `upserver` in production mode: 
```sh
docker compose -f docker-compose.yml -f docker-compose.prod.yml --profile all up --build -d
docker compose -f docker-compose.yml -f docker-compose.prod.yml --profile all down
```

 