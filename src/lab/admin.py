from django.contrib import admin

from lab.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = [
        "name",
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
    list_editable = [
        "cement_weight",
        "sand_weight",
        "gravel_weight",
        "water_weight",
        "admixture_weight",
    ]
