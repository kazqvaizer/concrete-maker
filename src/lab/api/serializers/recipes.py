from rest_framework import serializers

from lab.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "cement_weight",
            "sand_weight",
            "gravel_weight",
            "water_weight",
            "admixture_weight",
        ]
