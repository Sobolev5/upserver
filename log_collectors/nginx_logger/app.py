import os
import time
import gzip
import pika
import datetime
from loguru import logger
from dotenv import load_dotenv
from tinydb import TinyDB, Query


# ENV
load_dotenv()
AMQP_URI = os.getenv("AMQP_URI", "amqp://admin:admin@127.0.0.1:5672/vhost")
NGINX_LOG_DIR = os.getenv("NGINX_LOG_DIR", "/var/log/nginx")
DEBUG = os.getenv("DEBUG", False)
MAX_FILE_SIZE = 1048576 # 100MB


# DB
db = TinyDB('db.json')


def parse_nginx_log():
    now_date = datetime.datetime.now().date()
    for f in os.listdir(NGINX_LOG_DIR):

        f_path = os.path.join(NGINX_LOG_DIR, f)
        f_stat = os.stat(f_path)
        f_creation_date = datetime.datetime.strptime(time.ctime(f_stat.st_ctime), "%c").date()
        f_size = f_stat.st_size

        FName = Query()
        if not db.search(FName.name == f):
            if now_date == f_creation_date and f_size < MAX_FILE_SIZE and f.endswith(".gz"): 

                f_open = gzip.open(f_path, mode="rb")
                f_binary = f_open.read()
                f_open.close()

                logger.opt(colors=True).info(f"parse_nginx_log -> {f} read binary [ <green>OK</green> ]")
                connection = pika.BlockingConnection(pika.URLParameters(AMQP_URI))
                channel = connection.channel()
                channel.queue_declare(queue='nginx_log_collector')
                channel.basic_publish(exchange='', routing_key='nginx_log_collector', body=f_binary)
                connection.close()

                db.insert({'type': 'f_name', 'name': f})
                logger.opt(colors=True).info(f"parse_nginx_log -> {f} send rabbitmq [ <green>OK</green> ]")


if __name__ == "__main__":
    parse_nginx_log()