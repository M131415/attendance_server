from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.users.models import User
from apps.users.api.serializers.teacher_serializer import PasswordSerializer
from apps.users.api.serializers.student_serializer import (
    StudentSerializer, StudentListSerializer, 
    UpdateStudentSerializer,
)

class StudentViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = StudentSerializer
    list_serializer_class = StudentListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                            .filter(is_active=True, rol='STUDENT')\
                            .values('id', 'username', 'email', 'name',)
        return self.queryset
    
    @action(detail=False, methods=['post'],)
    def create_from_list(self, request):
        """
        Action que acepta una lista de usuarios para crear múltiples instancias.
        """
        data = request.data  # La lista de objetos JSON enviada por el cliente
        
        if not isinstance(data, list):
            return Response({"error": "Se esperaba una lista de estudiantes."}, status=status.HTTP_400_BAD_REQUEST)
        
        success = []
        errors = []

        for user in data:
            user_serializer = self.serializer_class(data=user)
            if user_serializer.is_valid():
                user_serializer.save()
                success.append({
                    'message': 'Usuario creado correctamente.',
                    'user': user_serializer.data
                })
            else:
                errors.append({
                    'user': user['username'],
                    'errors': user_serializer.errors
                })
        
        return Response({
            'success': success,
            'errors': errors
        }, status=status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED)
    
    @action(methods=['get'], detail=False)
    def search_student(self, request):
        username_or_name = request.query_params.get('username_or_name', '')
        student = User.objects.filter(
            Q(username__icontains=username_or_name)|
            Q(name__icontains=username_or_name),
            rol = 'STUDENT'
        )
        if student:
            student_serializer = self.serializer_class(student, many=True)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'mensaje': 'No se ha encontrado un Estudiante.'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            })
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Estudiante registrado correctamente.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Hay errores en el registro',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)
    
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateStudentSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Estudiante actualizado correctamente'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la actualización',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'Estudiante eliminado correctamente'
            })
        return Response({
            'message': 'No existe el estudiante que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)