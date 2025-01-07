
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.users import models
from apps.users.api.filters.user_filter import UserFilter
from apps.users.api.serializers.user_serializer import *

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    update_serializer_class = UpdateUserSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = UserFilter # Filtros
    ordering_fields = ['last_name', ]  # Ordenación
    search_fields   = ['username', 'name',] # Busqueda

    def get_queryset(self, pk=None):
        if pk is None:
            return models.User.objects.filter(is_active=True)
        return models.User.objects.filter(id=pk, is_active=True).first()

    @action(detail=False, methods=['post'],)
    def create_from_list(self, request):
        """
        Crea una lista de usuarios a partir de una lista de usuarios

        ejemplo de url: /users/users/create_from_list/
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

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        """
        Cambia la contraseña de un usuario

        ejemplo de url: /users/users/1/set_password/
        """
        user = self.get_queryset(pk)
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
        """
        Retorna una lista de usuarios

        ejemplo de url: /users/users/
        """
        users = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(users)
        serializer = self.list_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    def create(self, request):
        """
        Crea un usuario

        ejemplo de url: /users/users/
        """
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
        """
        Retorna un usuario
        
        ejemplo de url: /users/users/1/
        """
        user = self.get_queryset(pk)
        if user:
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Usuario con ese id!'}, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, pk=None):
        """
        Actualiza un usuario
        
        ejemplo de url: /users/users/1/
        """
        user = self.get_queryset(pk)
        user_serializer = self.update_serializer_class(user, data=request.data)
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
        """
        Elimina un usuario
        
        ejemplo de url: /users/users/1/
        """
        user = self.get_queryset(pk)      
        if user:
            user.is_active = False
            user.save()
            return Response({'message':'Usuario eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Usuario con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
