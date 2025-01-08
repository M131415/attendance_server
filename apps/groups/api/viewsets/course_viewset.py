from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.groups.api.serializers.course_serializer import CourseSerializer, CourseListSerializer, CourseUpdateSerializer

from apps.groups import models

from apps.users.permissions import IsAdminOrTeacherUser


class CourseViewSet(viewsets.ModelViewSet):
    """
        Este viewset gestiona la informacion de los cursos
    """
    serializer_class = CourseSerializer
    list_serializer_class = CourseListSerializer
    update_serializer_class = CourseUpdateSerializer

    permission_classes = [IsAdminOrTeacherUser,]

    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ['teacher', 'period', 'group', 'schedules__day_of_week', 'subject',] # Filtros
    #ordering_fields = ['last_name', ]  # Ordenación
    #search_fields   = ['name', 'name',] # Busqueda

    def get_queryset(self, pk=None, user=None):
        from apps.users.models import Roles
        
        if pk is None:
            if user.rol == Roles.TEACHER:
                return models.Course.objects.filter(teacher=user, state=True)
            return models.Course.objects.filter(state=True)
        return models.Course.objects.filter(id=pk, state=True).first()
    
    def list(self, request):
        courses = self.filter_queryset(self.get_queryset(user=request.user))
        page = self.paginate_queryset(courses)  # Aplica la paginación
        serializer = self.list_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Curso registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = self.get_queryset(pk)
        if course:
            course_serializer = self.serializer_class(course)
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Curso con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            course_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if course_serializer.is_valid():
                course_serializer.save()
                return Response({
                    'message':'Curso actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':course_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        course = self.get_queryset(pk)       
        if course:
            course.state = False
            course.save()
            return Response({'message':'Curso eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Curso con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
