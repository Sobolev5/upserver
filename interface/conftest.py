import re
import pytest
import settings
import typing as t
from settings import POSTGRES_DB
from settings import POSTGRES_HOST
from settings import POSTGRES_PASSWORD
from settings import POSTGRES_PORT
from settings import POSTGRES_USER


@pytest.fixture(autouse=True)
def override_settings(settings):
    settings.ALERTS = True
    settings.TEST = True


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
  
  
# Helpers
def extract_key_re(key: str, json_s: str) -> list:
    regexp = re.compile(f'(?<=\"{key}\": \").+?(?=\")')
    return [x for x in regexp.findall(json_s)] 


def extract_key(obj: t.Union[dict, list], key: str) -> list:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                yield v
            else:
                yield from extract_key(v, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_key(item, key)