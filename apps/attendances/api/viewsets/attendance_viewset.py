from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.attendances.api.serializers.attendance_serializer import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
     
    def list(self, request):
        attendance_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "attendances": attendance_serializer.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Asistencia registrada correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'Hay un error', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        attendance = self.get_queryset(pk)
        if attendance:
            attendance_serializer = AttendanceSerializer(attendance)
            return Response(attendance_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Asistencia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            attendance_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if attendance_serializer.is_valid():
                attendance_serializer.save()
                return Response({'message':'Asistencia actualizada correctamente!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':attendance_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        attendance = self.get_queryset().filter(id=pk).first() # get instance        
        if attendance:
            attendance.state = False
            attendance.save()
            return Response({'message':'Asistencia eliminada correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Asistencia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)