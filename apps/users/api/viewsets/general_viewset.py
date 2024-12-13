
from rest_framework import status, viewsets

from apps.users import models
from apps.users.api.serializers.general_serializer import CareerSerializer

class CareerViewSet(viewsets.ModelViewSet):
    queryset = models.Career.objects.filter(state=True)
    serializer_class = CareerSerializer