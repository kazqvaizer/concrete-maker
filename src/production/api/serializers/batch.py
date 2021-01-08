from rest_framework import serializers

from production.models import Batch


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = [
            "id",
            "recipe",
            "volume",
            "cement_weight",
            "sand_weight",
            "gravel_weight",
            "water_weight",
            "admixture_weight",
        ]
