from rest_framework.viewsets import ModelViewSet

from production.api.serializers import BatchSerializer
from production.models import Batch


class BatchViewSet(ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
