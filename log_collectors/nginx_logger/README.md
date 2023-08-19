# Collect log on nginx side
Copy `nginx_logger` folder in `/var/www/nginx_logger` on your server and modify `NGINX_DIR` in `app.py`

```sh
cd /var/www/nginx_logger
python -m venv env && source env/bin/activate
pip install -r requirements.txt
```

Next add this command to cron:
``` sh
echo '*/30 * * * * /var/www/nginx_logger/env/bin/python /var/www/nginx_logger/app.py &>/dev/null' >> /var/spool/cron/root 
```

# Collect logs on upserver side
For collect logs add this command to cron:
```sh
echo '* * * * * docker exec -i upserver-interface python /interface/run.py log_collector.tasks "run_every_minute()" &>/dev/null' >> /var/spool/cron/root 
```