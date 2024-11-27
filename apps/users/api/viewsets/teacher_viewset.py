from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.users.models import User
from apps.groups.api.serializers.course_serializer import CourseSerializer
from apps.users.api.serializers.teacher_serializer import (
    TeacherSerializer, TeacherListSerializer, 
    PasswordSerializer, UpdateTeacherSerializer,
)

class TeacherViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = TeacherSerializer
    list_serializer_class = TeacherListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                            .filter(is_active=True, rol='TEACHER')\
                            .values('id', 'username', 'email', 'name','last_name')
        return self.queryset
    
    def get_courses_by_teacher(self, teacher=None):
        if teacher is not None:
            return CourseSerializer.Meta.model.objects.filter(state=True, teacher=teacher)
    
    @action(detail=True, methods=['get'])
    def get_courses(self, request, pk=None):
        teacher = self.get_object(pk)

        if teacher:
            course = self.get_courses_by_teacher(teacher)
            course_serializer = CourseSerializer(course, many=True)
            return Response({"cursos" : course_serializer.data})
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el grupo'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'],)
    def create_from_list(self, request):
        """
        Action que acepta una lista de usuarios para crear múltiples instancias.
        """
        data = request.data  # La lista de objetos JSON enviada por el cliente
        
        if not isinstance(data, list):
            return Response({"error": "Se esperaba una lista de docentes."}, status=status.HTTP_400_BAD_REQUEST)
        
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
    def search_teacher(self, request):
        username_or_name = request.query_params.get('username_or_name', '')
        teacher = User.objects.filter(
            Q(username__icontains=username_or_name)|
            Q(name__icontains=username_or_name),
            rol = 'TEACHER'
        )
        if teacher:
            teacher_serializer = self.serializer_class(teacher, many=True)
            return Response(teacher_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'mensaje': 'No se ha encontrado un Docente.'
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
                'message': 'Usuario registrado correctamente.',
                'user': user_serializer.data
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
        user_serializer = UpdateTeacherSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la actualización',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'Usuario eliminado correctamente'
            })
        return Response({
            'message': 'No existe el usuario que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)