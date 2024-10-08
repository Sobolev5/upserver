import os
from pathlib import Path


from dotenv import load_dotenv

load_dotenv()


# ENV
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "1"
PROD = os.getenv("PROD") == "1"
ALERTS = os.getenv("ALERTS") == "1"
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
AMQP_URI = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/vhost"
)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if TELEGRAM_CHAT_IDS := os.getenv("TELEGRAM_CHAT_IDS"):
    TELEGRAM_CHAT_IDS = [int(x) for x in TELEGRAM_CHAT_IDS.split(",")]

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS")
if CSRF_TRUSTED_ORIGINS := os.getenv("CSRF_TRUSTED_ORIGINS"):
    CSRF_TRUSTED_ORIGINS = [
        str(x) for x in os.getenv("CSRF_TRUSTED_ORIGINS").split(",")
    ]

try:
    LOG_SIZE = int(os.getenv("LOG_SIZE"))
except (ValueError, TypeError):
    LOG_SIZE = 10000


# COMMON
ALLOWED_HOSTS = ["*"]
BASE_DIR = Path(__file__).resolve().parent
ROOT_URLCONF = "urls"
WSGI_APPLICATION = "wsgi.application"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "log_collector",
    "monitoring",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
        "PASSWORD": POSTGRES_PASSWORD,
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


def skip_static_requests(record):
    if isinstance(record.args[0], str):
        return not record.args[0].startswith("GET /static/")
    else:
        return False


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "skip_static_requests": {
            "()": "django.utils.log.CallbackFilter",
            "callback": skip_static_requests,
        }
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        }
    },
    "handlers": {
        "django.server": {
            "level": "INFO",
            "filters": ["skip_static_requests"],
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
