from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.users.models import User
from apps.users.api.serializers.teacher_serializer import (
    TeacherSerializer, TeacherListSerializer, 
    PasswordSerializer, UpdateTeacherSerializer,
)
from apps.groups.api.serializers.group_serializer import ClassGroupSerializer

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
                            .values('id', 'username', 'email', 'name',)
        return self.queryset
    
    def get_groups_by_teacher(self, teacher=None):
        if teacher is not None:
            return ClassGroupSerializer.Meta.model.objects.filter(state=True, teacher=teacher)
    
    @action(detail=True, methods=['get'])
    def get_groups(self, request, pk=None):
        teacher = self.get_object(pk)

        if teacher:
            groups = self.get_groups_by_teacher(teacher)
            groups_serializer = ClassGroupSerializer(groups, many=True)
            return Response({"groups" : groups_serializer.data})
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el docente'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['get'], detail=False)
    def search_teacher(self, request):
        username_or_name = request.query_params.get('username_or_name', '')
        student = User.objects.filter(
            Q(username__icontains=username_or_name)|
            Q(name__icontains=username_or_name),
            rol = 'TEACHER'
        )
        if student:
            student_serializer = self.serializer_class(student, many=True)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
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
                'message': 'Usuario registrado correctamente.'
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