# ruff: noqa: F403 F405

from django_base.settings.base import *

DEBUG = True

if not TESTING:
    import socket

    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        *MIDDLEWARE,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    # tricks to have debug toolbar when developing with docker
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]


MIDDLEWARE = [
    *MIDDLEWARE,
    "django_prometheus.middleware.PrometheusAfterMiddleware",  # MUST ALWAYS BE LAST
]
