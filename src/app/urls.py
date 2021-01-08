from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from lab.api.views import RecipeViewSet
from production.api.views import BatchViewSet

# Viewsets:

router_v1 = DefaultRouter()

# Lab viewsets

router_v1.register("lab/recipes", RecipeViewSet)

# Production viewsets

router_v1.register("production/batches", BatchViewSet)

api_v1 = (
    path("", include(router_v1.urls)),
    # Misc views
    path("healthchecks/", include("django_healthchecks.urls")),
)

urlpatterns = [
    path("api/v1/", include((api_v1, "api"), namespace="v1")),
    path("admin/", admin.site.urls),
]
