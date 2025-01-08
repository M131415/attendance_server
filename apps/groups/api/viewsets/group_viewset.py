from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from apps.groups.api.serializers.group_serializer import GroupSerializer, GroupListSerializer, GroupUpdateSerializer
from apps.attendances.api.serializers.enrollment_serializer import EnrollmentSerializer

from apps.groups import models

from apps.users.permissions import IsAdminOrStudentUser

# Clase para controlar el tamano de la consulta al metodo list()
class GroupPagination(PageNumberPagination):
    page_size = 50


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    list_serializer_class = GroupListSerializer
    update_serializer_class = GroupUpdateSerializer

    permission_classes = [IsAdminOrStudentUser,]

    filter_backends = [DjangoFilterBackend,]
    filterset_fields   = ['name', 'period', 'enrollments__student', 'enrollments__state'] # Filtros

    pagination_class = GroupPagination

    def get_queryset(self, pk=None):
        if pk is None:
            return models.Group.objects.filter(state=True)
        return models.Group.objects.filter(id=pk, state=True).first()
    
    @action(detail=True, methods=['post'], url_path='enroll')
    def enroll_students(self, request, pk=None):
        """
        Inscribir a una lista de estudiantes en un grupo.
        """
        group = self.get_queryset(pk)
        
        if 'students' not in request.data.keys():
            return Response({"detail": "Se esperaba la palabra clave 'students' en la solicitud"}, status=status.HTTP_400_BAD_REQUEST)

        students_data = request.data.get('students', [])  # Lista de estudiantes (IDs)

        if not isinstance(students_data, list):
            return Response({"detail": "Se esperaba una lista de ids de los estudiantes."}, status=status.HTTP_400_BAD_REQUEST)
        
        enrollments = []
        errors = []

        for student_id in students_data:
            
            enrollment_serializer = EnrollmentSerializer(
                data = {
                    'group': group.id,
                    'student': student_id
                }
            )
            
            if enrollment_serializer.is_valid():
                enrollment_serializer.save()
                enrollments.append({
                    'message': 'inscripcion creado correctamente.',
                    'enrollment': enrollment_serializer.data
                })
            else:
                errors.append({
                    'student_id': student_id,
                    'errors': enrollment_serializer.errors
                })


        return Response({
            'enrollments': enrollments,
            'errors': errors
        }, status=status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'], url_path='unenroll')
    def unenroll_students(self, request, pk=None):
        """
        Desinscribir estudiantes de este grupo (marcar inscripción como inactiva).
        """
        
        if 'enrollments' not in request.data.keys():
            return Response({"detail": "Se esperaba la palabra clave 'enrollments' en la solicitud"}, status=status.HTTP_400_BAD_REQUEST)

        enrollment_ids = request.data.get('enrollments', [])  # Lista de IDs de inscripciones

        if not isinstance(enrollment_ids, list):
            return Response({"detail": "Se esperaba una lista de IDs de inscripciones."}, status=status.HTTP_400_BAD_REQUEST)

        deleted = []
        errors = []

        for enrollment_id in enrollment_ids:
            
            # Obtener la inscripción
            enrollment = EnrollmentSerializer.Meta.model.objects.filter(id=enrollment_id).first()

            # Marcar la inscripción como inactiva
            if enrollment:
                enrollment.state = False
                enrollment.save()
                deleted.append(enrollment_id)
            else:
                errors.append({"enrollment": enrollment_id, "error": 'No existe una Inscripción con estos datos!'})

        return Response({
            "deleted": deleted,
            "errors": errors,
        }, status=status.HTTP_200_OK if deleted else status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        print(request.user)
        groups = self.filter_queryset(self.get_queryset()) # Aplica los filtros
        page = self.paginate_queryset(groups)  # Aplica la paginación
        serializer = self.list_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
        
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Grupo de clase registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        group = self.get_queryset(pk)
        if group:
            group_serializer = self.serializer_class(group)
            return Response(group_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Grupo de clase con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            group_serializer = self.update_serializer_class(self.get_queryset(pk), data=request.data)           
            if group_serializer.is_valid():
                group_serializer.save()
                return Response({
                    'message':'Grupo de clase actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':group_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        group = self.get_queryset(pk)       
        if group:
            group.state = False
            group.save()
            return Response({'message':'Grupo de clase eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Grupo de clase con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
