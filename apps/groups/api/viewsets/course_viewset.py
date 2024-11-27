from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.groups.api.serializers.course_serializer import CourseSerializer, CourseRetrieveSerializer
from apps.groups.api.serializers.general_serializers import ScheduleSerializer
from apps.attendances.api.serializers.enrollment_serializer import EnrollmentSerializer
from apps.attendances.api.serializers.attendance_serializer import AttendanceSerializer

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    
    def get_schedule_by_group(self, course=None):
        if course is not None:
            return ScheduleSerializer.Meta.model.objects.filter(state=True, course=course)
    
    @action(detail=True, methods=['get'])
    def get_schedule(self, request, pk=None):
        course = self.get_queryset(pk)

        if course:
            schedule = self.get_schedule_by_group(course)
            schedule_serializer = ScheduleSerializer(schedule, many=True)
            return Response({"schedules" : schedule_serializer.data})
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el grupo'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_attendances_by_group(self, course=None):
        if course is not None:
            return AttendanceSerializer.Meta.model.objects.filter(state=True, course=course)
    
    @action(detail=True, methods=['get'])
    def get_attendances(self, request, pk=None):
        course = self.get_queryset(pk)

        if course:
            attendance = self.get_attendances_by_group(course)
            attendance_serializer = AttendanceSerializer(attendance, many=True)
            return Response({"attendances" : attendance_serializer.data})
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el grupo'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_enrollments_by_group(self, course=None):
        if course is not None:
            return EnrollmentSerializer.Meta.model.objects.filter(state=True, group=course.group)
    
    @action(detail=True, methods=['get'])
    def get_enrollments(self, request, pk=None):
        course = self.get_queryset(pk)

        if course:
            schedule = self.get_enrollments_by_group(course)
            schedule_serializer = EnrollmentSerializer(schedule, many=True)
            return Response({"enrollments" : schedule_serializer.data})
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el grupo'
        }, status=status.HTTP_400_BAD_REQUEST)

        
    def list(self, request):
        course_serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            "total": self.get_queryset().count(),
            "courses": course_serializer.data
        }
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Curso registrado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response({'message':'', 'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = self.get_queryset(pk)
        if course:
            course_serializer = CourseRetrieveSerializer(course)
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Curso con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset(pk):
            course_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if course_serializer.is_valid():
                course_serializer.save()
                return Response({'message':'Curso actualizado correctamente!'}, status=status.HTTP_200_OK)
            return Response({'message':'', 'error':course_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   

    def destroy(self, request, pk=None):       
        course = self.get_queryset().filter(id=pk).first() # get instance        
        if course:
            course.state = False
            course.save()
            return Response({'message':'Curso eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Curso con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
