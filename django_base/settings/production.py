# ruff: noqa: F403 F405

from django_base.settings.base import *

DEBUG = False


MIDDLEWARE = [
    *MIDDLEWARE,
    "django_prometheus.middleware.PrometheusAfterMiddleware",  # MUST ALWAYS BE LAST
]
