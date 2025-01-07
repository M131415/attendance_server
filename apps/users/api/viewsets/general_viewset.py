
from rest_framework import viewsets

from apps.users import models
from apps.users.api.serializers.general_serializer import CareerSerializer

class CareerViewSet(viewsets.ModelViewSet):
    serializer_class = CareerSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return models.Career.objects.filter(state=True)
        return models.Career.objects.filter(id=pk, state=True).first()