"""https://docs.djangoproject.com/en/5.0/topics/http/urls/"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

#### Apps
urlpatterns = [
    path("admin/", admin.site.urls),
]

#### 3rd party urls
urlpatterns = [
    *urlpatterns,
    path("prometheus/", include("django_prometheus.urls")),
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

#### Static files serving for local development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#### Django Debug Toolbar
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
