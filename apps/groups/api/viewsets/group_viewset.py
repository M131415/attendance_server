from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser

from apps.groups.api.serializers.group_serializer import *
from apps.groups.api.serializers.general_serializers import ScheduleSerializer

class ClassGroupViewSet(viewsets.ModelViewSet):
    serializer_class = ClassGroupSerializer
    parser_classes = (JSONParser, MultiPartParser, )

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    def get_schedule_by_group(self, class_group=None):
        if class_group is not None:
            return ScheduleSerializer.Meta.model.objects.filter(state=True, group=class_group)
    
    @action(detail=True, methods=['get'])
    def get_schedule(self, request, pk=None):
        class_group = self.get_queryset(pk)

        if class_group:
            schedule = self.get_schedule_by_group(class_group)
            schedule_serializer = ScheduleSerializer(schedule, many=True)
            return Response({"schedules" : schedule_serializer.data})
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el grupo'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request):
        class_group_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "class_groups": class_group_serializer.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Grupo de clase registrado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        class_group = self.get_queryset(pk)
        if class_group:
            class_group_serializer = ClassGroupRetrieveSerializer(class_group)
            return Response(class_group_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Grupo de clase con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            class_group_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if class_group_serializer.is_valid():
                class_group_serializer.save()
                return Response({'message':'Grupo de clase actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':class_group_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        class_group = self.get_queryset().filter(id=pk).first() # get instance        
        if class_group:
            class_group.state = False
            class_group.save()
            return Response({'message':'Grupo de clase eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Grupo de clase con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
