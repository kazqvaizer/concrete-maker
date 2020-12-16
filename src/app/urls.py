from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("api/v1/healthchecks/", include("django_healthchecks.urls")),
    path("admin/", admin.site.urls),
]
