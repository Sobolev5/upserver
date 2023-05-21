# Development commands

Get logs:
```sh
docker compose logs -f upserver-interface upserver-alerts
docker compose logs -f upserver-monitoring
``` 

Run cron:
```sh
docker exec upserver-interface python /interface/run.py log_collector.tasks "run_every_minute()"
docker exec upserver-alerts python /alerts/run.py 
``` 

 