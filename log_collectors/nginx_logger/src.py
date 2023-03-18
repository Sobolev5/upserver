import datetime
import json
from throw_catch import throw

AMQP_URI = f"amqp://admin:admin@127.0.0.1:5672/vhost"
BATCH_SIZE = 1000
BATCH_COUNTER = 0
LOG_FILE = "/var/log/nginx/access.log"


def parse_nginx_log():
    datetime_now = datetime.datetime.now()
    day_ago = datetime_now - datetime.timedelta(days=1)
    day_ago  = day_ago.strftime("%Y-%m-%d")
    
    try:
        with open(LOG_FILE) as f:
            payload = None
            for line in f:
                try:
                    payload = json.loads(line)
                except:
                    continue
                
                payload["request_timestamp"] = datetime.datetime.fromisoformat(payload["request_timestamp"]).replace(tzinfo=None).strftime("%Y-%m-%d %H:%M:%S")
                payload["http_user_agent"] = "%s..." % payload["http_user_agent"][:40]
                payload["request_uri"] = "%s..." % payload["request_uri"][:200]
            
                if "url" in payload["request_uri"]:
                    continue

                if not payload["scheme"]:
                    payload["scheme"] = "http"  

                if not payload["request_method"]:
                    payload["request_method"] = "UNKNOWN"    

                strip_dict = {}
                for k, v in payload.items():
                    if isinstance(v, str):
                        v = v.strip()
                    strip_dict[k] = v
                payload = strip_dict

                BATCH_COUNTER += 1
                if BATCH_COUNTER % BATCH_SIZE == 0:
                    try:
                        # TODO throw
                        print(f'ok {BATCH_SIZE}')
                    except Exception as e:
                        print(e)
                        continue
                
            if payload:
                # last records
                try:
                    # TODO throw
                    print(f'ok {BATCH_SIZE}')
                except Exception as e:
                    print(e)
                
            f = open(LOG_FILE, "w+")
            f.truncate()
            f.close()
    except:
        f = open(LOG_FILE, "w+")
        f.truncate()
        f.close()

if __name__ == "__main__":
    parse_nginx_log()