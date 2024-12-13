from rest_framework import status, viewsets
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.groups.api.serializers.general_serializers import *

from apps.groups import models

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = models.Subject.objects.filter(state=True)
    serializer_class = SubjecSerializer

    filter_backends = [DjangoFilterBackend,]
    filterset_fields   = ['code', 'name'] # Filtros
   
    def list(self, request):
        subjects = self.filter_queryset(self.get_queryset()) # Aplica los filtros
        page = self.paginate_queryset(subjects)  # Aplica la paginación
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Materia registrada correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors}
        , status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        subject = self.get_queryset().filter(id=pk,).first()
        if subject:
            subject_serializer = self.serializer_class(subject)
            return Response(subject_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Materia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset().filter(id=pk,).first():
            subject_serializer = self.serializer_class(self.get_queryset().filter(id=pk,).first(), data=request.data)           
            if subject_serializer.is_valid():
                subject_serializer.save()
                return Response({
                    'message':'Materia actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':subject_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        subject = self.get_queryset().filter(id=pk,).first()       
        if subject:
            subject.state = False
            subject.save()
            return Response({'message':'Materia eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Materia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

class DepartamentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.filter(state=True)
    serializer_class = DepartamentSerializer
   
    def list(self, request):
        departments = self.filter_queryset(self.get_queryset()) # Aplica los filtros
        page = self.paginate_queryset(departments)  # Aplica la paginación
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Departamento registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        department = self.get_queryset().filter(id=pk,).first()
        if department:
            department_serializer = self.serializer_class(department)
            return Response(department_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Departamento con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None): 
        if self.get_queryset().filter(id=pk,).first():
            department_serializer = self.serializer_class(self.get_queryset().filter(id=pk,).first(), data=request.data)           
            if department_serializer.is_valid():
                department_serializer.save()
                return Response({
                    'message':'Departamento actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':department_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        department = self.get_queryset().filter(id=pk,).first()       
        if department:
            department.state = False
            department.save()
            return Response({'message':'Departamento eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Departamento con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

class PeriodViewSet(viewsets.ModelViewSet):
    queryset = models.Period.objects.filter(state=True)
    serializer_class = PeriodSerializer
   
    def list(self, request):
        periods = self.filter_queryset(self.get_queryset()) # Aplica los filtros
        page = self.paginate_queryset(periods)  # Aplica la paginación
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Periodo registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        period = self.get_queryset().filter(id=pk,).first()
        if period:
            period_serializer = self.serializer_class(period)
            return Response(period_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Periodo con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset().filter(id=pk,).first():
            period_serializer = self.serializer_class(self.get_queryset().filter(id=pk,).first(), data=request.data)           
            if period_serializer.is_valid():
                period_serializer.save()
                return Response({
                    'message':'Periodo actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':period_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        period = self.get_queryset().filter(id=pk,).first()       
        if period:
            period.state = False
            period.save()
            return Response({'message':'Periodo eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Periodo con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

class SchoolRoomViewSet(viewsets.ModelViewSet):
    queryset = models.SchoolRoom.objects.filter(state=True)
    serializer_class = SchoolRoomSerializer

    filter_backends = [DjangoFilterBackend,]
    filterset_fields   = ['name'] # Filtros
   
    def list(self, request):
        school_room = self.filter_queryset(self.get_queryset()) # Aplica los filtros
        page = self.paginate_queryset(school_room)  # Aplica la paginación
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Aula de clases registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        school_room = self.get_queryset().filter(id=pk,).first()
        if school_room:
            school_room_serializer = self.serializer_class(school_room)
            return Response(school_room_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Aula de clases con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset().filter(id=pk,).first():
            school_room_serializer = self.serializer_class(self.get_queryset().filter(id=pk,).first(), data=request.data)           
            if school_room_serializer.is_valid():
                school_room_serializer.save()
                return Response({
                    'message':'Aula de clases actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':school_room_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        school_room = self.get_queryset().filter(id=pk,).first()       
        if school_room:
            school_room.state = False
            school_room.save()
            return Response({'message':'Aula de clases eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Aula de clases con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = models.Schedule.objects.filter(state=True)
    serializer_class = ScheduleSerializer
    list_serializer_class = ScheduleListSerializer

    def list(self, request):
        schedules = self.filter_queryset(self.get_queryset()) # Aplica los filtros
        page = self.paginate_queryset(schedules)  # Aplica la paginación
        serializer = self.list_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Horario registrado correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        schedule = self.get_queryset().filter(id=pk,).first()
        if schedule:
            schedule_serializer = self.serializer_class(schedule)
            return Response(schedule_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Horario con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset().filter(id=pk,).first():
            schedule_serializer = self.serializer_class(self.get_queryset().filter(id=pk,).first(), data=request.data)           
            if schedule_serializer.is_valid():
                schedule_serializer.save()
                return Response({
                    'message':'Horario actualizado correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':schedule_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        schedule = self.get_queryset().filter(id=pk,).first()       
        if schedule:
            schedule.state = False
            schedule.save()
            return Response({'message':'Horario eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Horario con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
