import os

from dotenv import load_dotenv
load_dotenv()

DEBUG = os.getenv("DEBUG") == "1"
TEST = os.getenv("TEST") == "1"
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
AMQP_URI = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/vhost"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

try:
    TELEGRAM_CHAT_IDS = [int(x) for x in os.getenv("TELEGRAM_CHAT_IDS").split(',')]
except:
    TELEGRAM_CHAT_IDS = []       