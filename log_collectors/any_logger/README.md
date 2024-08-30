# upserver-any-logger

For collect `AnyLogger` add this command to cron:
```sh
echo '* * * * * docker exec upserver-interface python /interface/run.py log_collector.tasks "run_every_minute()" &>/dev/null' >> /var/spool/cron/root 