from django.urls import include, path

urlpatterns = [
    path("recofy/", include(("apps.recofy.urls", "recofy"))),
]
