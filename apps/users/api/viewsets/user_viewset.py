
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.users import models
from apps.users.api.filters.user_filter import UserFilter
from apps.users.api.serializers.user_serializer import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = UserFilter # Filtros
    ordering_fields = ['last_name', ]  # Ordenación
    search_fields   = ['username', 'name',] # Busqueda

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

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_queryset().filter(id=pk,).first()
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
        users = self.filter_queryset(self.get_queryset())  # Aplica filtros y ordering
        user_serializer = self.list_serializer_class(users, many=True)
        return Response(user_serializer.data)
    
    def create(self, request):
        print(request.data)
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
        user = self.get_queryset().filter(id=pk,).first()
        if user:
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Usuario con ese id!'}, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, pk=None):
        user = self.get_queryset().filter(id=pk,).first()
        user_serializer = UpdateUserSerializer(user, data=request.data)
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
        user = self.get_queryset().filter(id=pk,).first()      
        if user:
            user.is_active = False
            user.save()
            return Response({'message':'Usuario eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Usuario con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
