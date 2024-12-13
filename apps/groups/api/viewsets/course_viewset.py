from collections import defaultdict
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.groups.api.serializers.course_serializer import CourseSerializer, CourseListSerializer, CourseUpdateSerializer
from apps.attendances.api.serializers.attendance_serializer import TakeAttendanceSerializer

from apps.groups import models

class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.filter(state=True)
    serializer_class = CourseSerializer
    list_serializer_class = CourseListSerializer
    update_serializer_class = CourseUpdateSerializer

                                  
    def get_attendances_by_course(self, course=None):
        if course is not None:
            return TakeAttendanceSerializer.Meta.model.objects.filter(state=True, course=course)
    
    @action(detail=True, methods=['get'])
    def get_attendances(self, request, pk=None):
        course = self.get_queryset().filter(id=pk,).first()

        if course:
            # Obtén las asistencias del curso
            attendance_queryset = self.get_attendances_by_course(course)

            #Obtener los dias de asistencia
            days = []
            for attendance in attendance_queryset:
                days.append(attendance.attendance_date.strftime('%Y-%m-%d'))

            print(days)

            # Procesa los datos para agruparlos
            attendance_data = defaultdict(lambda: defaultdict(int))
            total_count = 0

            for record in attendance_queryset:
                date = record.attendance_date.strftime('%Y-%m-%d')
                attendance_status = record.attendance_status
                attendance_data[date][attendance_status] += 1
                total_count += 1

            # Convierte el defaultdict a un dict normal para JSON
            attendances_by_date = {
                date: dict(status_counts) for date, status_counts in attendance_data.items()
            }

            # Arma la respuesta final
            response_data = {
                "attendances": {
                    "total_count": total_count,
                    "total_days": len(attendance_data),
                    "days" : attendances_by_date
                }
            }
            return Response(response_data)
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': 'No existe el curso'
        }, status=status.HTTP_400_BAD_REQUEST)

        
    

    @action(detail=True, methods=['post'], url_path='take_attendances')
    def take_attendances(self, request, pk=None):
        """
        Pasar lista a una lista de inscripciones del grupo de un curso
        """
        course = self.get_queryset().filter(id=pk,).first()
        
        if 'attendances' not in request.data.keys():
            return Response({"detail": "Se esperaba la palabra clave 'attendances' en la solicitud"}, status=status.HTTP_400_BAD_REQUEST)

        take_attendance_data = request.data.get('attendances', [])  # Lista de asistencias sin el curso

        if not isinstance(take_attendance_data, list):
            return Response({"detail": "Se esperaba una lista de asistencias."}, status=status.HTTP_400_BAD_REQUEST)
        
        attendances = []
        errors = []

        for take_attendande in take_attendance_data:
            
            take_attendance_serializer = TakeAttendanceSerializer(
                data = {
                    'course': course.id,
                    'enrollment': take_attendande['enrollment'],
                    'observation': take_attendande['observation'],
                    'attendance_date': take_attendande['attendance_date'],
                    'attendance_status': take_attendande['attendance_status'],
                }
            )
            
            if take_attendance_serializer.is_valid():
                take_attendance_serializer.save()
                attendances.append({
                    'message': 'Asistencia creado correctamente.',
                    'attendance': take_attendance_serializer.data
                })
            else:
                errors.append({
                    'enrollment_id': take_attendande['enrollment'],
                    'errors': take_attendance_serializer.errors
                })

        return Response({
            'attendances': attendances,
            'errors': errors
        }, status=status.HTTP_207_MULTI_STATUS if errors else status.HTTP_201_CREATED)
    
    def list(self, request):
        courses = self.filter_queryset(self.get_queryset())
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
        course = self.get_queryset().filter(id=pk,).first()
        if course:
            course_serializer = self.serializer_class(course)
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Curso con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       if self.get_queryset().filter(id=pk,).first():
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
        course = self.get_queryset().filter(id=pk).first() # get instance        
        if course:
            course.state = False
            course.save()
            return Response({'message':'Curso eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe un Curso con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)
