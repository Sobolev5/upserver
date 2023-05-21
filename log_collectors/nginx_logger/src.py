import re
import os
import time
import gzip
import pika
import datetime
import pickle
from dotenv import load_dotenv


load_dotenv()


AMQP_URI = os.getenv("AMQP_URI", "amqp://admin:admin@127.0.0.1:5672/vhost")
NGINX_LOG_DIR = os.getenv("NGINX_LOG_DIR", "/var/log/nginx")
DEBUG = os.getenv("DEBUG", False)


def parse_nginx_log():
    now_date = datetime.datetime.now().date()
    for f in os.listdir(NGINX_LOG_DIR):
        f_path = os.path.join(NGINX_LOG_DIR, f)
        f_creation_date = datetime.datetime.strptime(time.ctime(os.path.getctime(f_path)), "%c").date()
        if now_date == f_creation_date:

            if f.endswith(".gz"):
                f_open = gzip.open(f_path, mode="rb")
            else:
                f_open = open(f_path, mode="rb")
            f_binary = f_open.read()
            f_open.close()

            connection = pika.BlockingConnection(pika.URLParameters(AMQP_URI))
            channel = connection.channel()
            channel.queue_declare(queue='nginx_log_collector')
            channel.basic_publish(exchange='', routing_key='nginx_log_collector', body=f_binary)
            connection.close()

            if DEBUG:
                print("OK")


if __name__ == "__main__":
    parse_nginx_log()