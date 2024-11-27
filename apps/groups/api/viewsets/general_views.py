from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.groups.models import Subject, Departament, Period, SchoolRoom, Schedule
from apps.groups.api.serializers.general_serializers import *

class SubjectViewSet(viewsets.GenericViewSet):
    model = Subject
    serializer_class = SubjecSerializer
   
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'], state=True)

    def list(self, request):
        subject = self.get_queryset()
        subject_serializer = self.get_serializer(subject, many=True)
        data = {
            "total": self.get_queryset().count(),
            "subjects": subject_serializer.data
        }
        return Response(data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Materia registrada correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Materia no encontrada!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():       
                serializer.save()       
                return Response({'message':'Materia actualizada correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():       
            self.get_object().get().delete()       
            return Response({'message':'Materia eliminada correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Materia no encontrada!'}, status=status.HTTP_400_BAD_REQUEST)

class DepartamentViewSet(viewsets.GenericViewSet):
    model = Departament
    serializer_class = DepartamentSerializer
   
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'], state=True)

    def list(self, request):
        departament = self.get_queryset()
        departament_serializer = self.get_serializer(departament, many=True)
        data = {
            "total": self.get_queryset().count(),
            "departaments": departament_serializer.data
        }
        return Response(data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Periodo registrado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Periodo no encontrado!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None): 
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():       
                serializer.save()       
                return Response({'message':'Periodo actualizado correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():       
            self.get_object().get().delete()       
            return Response({'message':'Periodo eliminado correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Materia no encontrada!'}, status=status.HTTP_400_BAD_REQUEST)

class PeriodViewSet(viewsets.GenericViewSet):
    model = Period
    serializer_class = PeriodSerializer
   
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'], state=True)

    def list(self, request):
        period = self.get_queryset()
        period_serializer = self.get_serializer(period, many=True)
        data = {
            "total": self.get_queryset().count(),
            "periods": period_serializer.data
        }
        return Response(data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Periodo registrado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Periodo no encontrado!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():       
                serializer.save()       
                return Response({'message':'Periodo actualizado correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():       
            self.get_object().get().delete()       
            return Response({'message':'Periodo eliminado correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Periodo no encontradao'}, status=status.HTTP_400_BAD_REQUEST)

class SchoolRoomViewSet(viewsets.GenericViewSet):
    model = SchoolRoom
    serializer_class = SchoolRoomSerializer
   
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'], state=True)

    def list(self, request):
        school_room = self.get_queryset()
        school_room_serializer = self.get_serializer(school_room, many=True)
        data = {
            "total": self.get_queryset().count(),
            "schoolRooms": school_room_serializer.data
        }
        return Response(data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Aula registrada correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Aula no encontrada!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():       
                serializer.save()       
                return Response({'message':'Aula actualizada correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():       
            self.get_object().get().delete()       
            return Response({'message':'Aula eliminada correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Materia no encontrada!'}, status=status.HTTP_400_BAD_REQUEST)

class ScheduleViewSet(viewsets.GenericViewSet):
    model = Schedule
    serializer_class = ScheduleSerializer
   
    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True)

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'], state=True)

    def list(self, request):
        schedules = self.get_queryset()
        schedule_serializer = self.get_serializer(schedules, many=True)
        data = {
            "total": self.get_queryset().count(),
            "schedules": schedule_serializer.data
        }
        return Response(data)
        

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Horario registrado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if self.get_object().exists():
            data = self.get_object().get()
            data = self.get_serializer(data)
            return Response(data.data)
        return Response({'message':'', 'error':'Horario no encontrado!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)       
            if serializer.is_valid():       
                serializer.save()       
                return Response({'message':'Horario actualizado correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    

    def destroy(self, request, pk=None):       
        if self.get_object().exists():
            self.get_object().get().delete()       
            return Response({'message':'Horario eliminado correctamente!'}, status=status.HTTP_200_OK)       
        return Response({'message':'', 'error':'Horario no encontrado!'}, status=status.HTTP_400_BAD_REQUEST)
    
class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

        
    def list(self, request):
        class_group_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "groups": class_group_serializer.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Grupo de clase registrado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        class_group = self.get_queryset(pk)
        if class_group:
            class_group_serializer = ClassGroupRetrieveSerializer(class_group)
            return Response(class_group_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Grupo de clase con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            class_group_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if class_group_serializer.is_valid():
                class_group_serializer.save()
                return Response({'message':'Grupo de clase actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':class_group_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        class_group = self.get_queryset().filter(id=pk).first() # get instance        
        if class_group:
            class_group.state = False
            class_group.save()
            return Response({'message':'Grupo de clase eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Grupo de clase con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
