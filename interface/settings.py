import os
from pathlib import Path


from dotenv import load_dotenv
load_dotenv()


# ENV
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "1"
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_IDS = os.getenv("TELEGRAM_CHAT_IDS", [])
try:
    LOG_SIZE = int(os.getenv("LOG_SIZE"))
except:
    LOG_SIZE = 10000


# COMMON
ALLOWED_HOSTS = ['*']
BASE_DIR = Path(__file__).resolve().parent
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'integrations',
    'monitoring'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# INTEGRATION DJANGO CLICKHOUSE LOGGER https://github.com/Sobolev5/django-clickhouse-logger
CLICKHOUSE_LOGGER_ENABLED = os.getenv("CLICKHOUSE_LOGGER_ENABLED")  == "1"  # SWITCH TO 1 IN .ENV FILE IF YOU WANT TO USE THIS INTEGRATION
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD") 
if CLICKHOUSE_HOST and CLICKHOUSE_LOGGER_ENABLED:
    DJANGO_CLICKHOUSE_LOGGER_HOST = CLICKHOUSE_HOST
    DJANGO_CLICKHOUSE_LOGGER_PORT = CLICKHOUSE_PORT
    DJANGO_CLICKHOUSE_LOGGER_USER = CLICKHOUSE_USER
    DJANGO_CLICKHOUSE_LOGGER_PASSWORD = CLICKHOUSE_PASSWORD
    DJANGO_CLICKHOUSE_LOGGER_TTL_DAY = 3


# INTEGRATION SIMPLE PRINT https://github.com/Sobolev5/simple-print]
SIMPLE_PRINT_ENABLED = os.getenv("SIMPLE_PRINT_ENABLED") == "1" # SWITCH TO 1 IN .ENV FILE IF YOU WANT TO USE THIS INTEGRATION
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
AMQP_URI = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/vhost"
if RABBITMQ_HOST and SIMPLE_PRINT_ENABLED:
    SIMPLE_PRINT_AMQP_URI = AMQP_URI
