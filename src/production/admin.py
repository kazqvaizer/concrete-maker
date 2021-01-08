from django.contrib import admin

from production.models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    fields = [
        "recipe",
        "volume",
        "cement_weight",
        "sand_weight",
        "gravel_weight",
        "water_weight",
        "admixture_weight",
    ]
    list_display = [
        "__str__",
        "cement_weight",
        "sand_weight",
        "gravel_weight",
        "water_weight",
        "admixture_weight",
    ]
