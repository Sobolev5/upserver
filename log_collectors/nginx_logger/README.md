# Collect logs on upserver side
For collect logs add this command to cron:
```sh
echo '* * * * * docker exec -i upserver-interface python /app/run.py log_collector.tasks "run_every_minute()" &>/dev/null' >> /var/spool/cron/root 