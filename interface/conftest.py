import pytest
from django.contrib.auth.models import User
from userprofiles.models import Profile

import settings
from settings import POSTGRES_DB
from settings import POSTGRES_HOST
from settings import POSTGRES_PASSWORD
from settings import POSTGRES_PORT
from settings import POSTGRES_USER


@pytest.fixture(autouse=True)
def override_settings(settings):
    settings.ALERTS = False


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
        "ATOMIC_REQUESTS": False
    }
  
