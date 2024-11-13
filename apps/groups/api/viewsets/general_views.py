from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.groups.models import Subject, Departament, Period, SchoolRoom
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
        subject = self.get_queryset()
        subject_serializer = self.get_serializer(subject, many=True)
        data = {
            "total": self.get_queryset().count(),
            "periods": subject_serializer.data
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
        subject = self.get_queryset()
        subject_serializer = self.get_serializer(subject, many=True)
        data = {
            "total": self.get_queryset().count(),
            "schoolRooms": subject_serializer.data
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
