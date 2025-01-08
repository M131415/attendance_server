from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from apps.attendances.api.serializers.enrollment_serializer import EnrollmentListSerializer, EnrollmentSerializer
from apps.attendances import models

from apps.users.permissions import IsAdminOrStudentUser

class EnrollomentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    list_serializer_class = EnrollmentListSerializer

    permission_classes = [IsAdminOrStudentUser,]

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['student', 'group',] # Filtros

    def get_queryset(self, pk=None):
        if pk is None:
            return models.Enrollment.objects.filter(state=True)
        return models.Enrollment.objects.filter(id=pk, state=True).first()
        
    def list(self, request):
        """
            Retorna una lista de todas las inscripciones activas

            ejemplo de url: /attendances/enrollments/
        """
        enrollments = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(enrollments) 
        serializer = self.list_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        """
            Crea una inscripcion con la información enviada en el request 

            ejemplo de url: /attendances/enrollments/
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Inscripción registrada correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'Hay un error', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
            Retorna la información de una inscripción activa

            ejemplo de url: /attendances/enrollments/1/
        """
        enrollment = self.get_queryset(pk)
        if enrollment:
            enrollment_serializer = self.serializer_class(enrollment)
            return Response(enrollment_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Inscripción con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       """
            Actualiza la información de una inscripción activa

            ejemplo de url: /attendances/enrollments/1/
        """
       if self.get_queryset(pk):
            enrollment_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if enrollment_serializer.is_valid():
                enrollment_serializer.save()
                return Response({
                    'message':'Inscripción actualizada correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':enrollment_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):
        """
            Actualiza el estado de una inscripción a inactiva

            ejemplo de url: /attendances/enrollments/1/
        """
        enrollment = self.get_queryset(pk)  
        if enrollment:
            enrollment.state = False
            enrollment.save()
            return Response({'message':'Inscripción eliminada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Inscripción con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)