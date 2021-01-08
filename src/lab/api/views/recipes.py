from rest_framework.viewsets import ModelViewSet

from lab.api.serializers import RecipeSerializer
from lab.models import Recipe


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
