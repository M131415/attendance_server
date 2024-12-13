from rest_framework import status, viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from apps.attendances.api.serializers.attendance_serializer import AttendanceSerializer

from apps.attendances import models

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = models.Attendance.objects.filter(state=True)
    serializer_class = AttendanceSerializer

    filter_backends = [DjangoFilterBackend,]
    filterset_fields   = ['course', 'enrollment'] # Filtros
  
    def list(self, request):
        attendances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(attendances)  # Aplica la paginación
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Asistencia registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        attendance = self.get_queryset().filter(id=pk,).first()
        if attendance:
            attendance_serializer = self.serializer_class(attendance)
            return Response(attendance_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Asistencia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset().filter(id=pk,).first():
            attendance_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if attendance_serializer.is_valid():
                attendance_serializer.save()
                return Response({
                    'message':'Asistencia actualizada correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':attendance_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)  

    def destroy(self, request, pk=None):       
        attendance = self.get_queryset().filter(id=pk).first() # get instance        
        if attendance:
            attendance.state = False
            attendance.save()
            return Response({'message':'Asistencia eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Asistencia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
