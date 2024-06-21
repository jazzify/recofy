# ruff: noqa: F403 F405

from django_base.settings.base import *

DEBUG = False

MIDDLEWARE = [
    *MIDDLEWARE,
    "django_prometheus.middleware.PrometheusAfterMiddleware",  # Must always be last
]

CSRF_TRUSTED_ORIGINS = ["http://nginx:8080"]
