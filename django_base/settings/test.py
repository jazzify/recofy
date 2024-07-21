# ruff: noqa: F403 F405
from django_base.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "local_test_db",
    }
}
