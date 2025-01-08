import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime

from apps.attendances.api.serializers.attendance_serializer import AttendanceListSerializer, TakeAttendancesCourseSerializer, AttendanceSerializer, AttendanceReportSerializer

from apps.attendances import models
from apps.groups.models import Course

from rest_framework.permissions import IsAuthenticated

class AttendanceViewSet(viewsets.ModelViewSet):
    """
        En este ViewSet ademas de gestinar las asistencias
    """
    serializer_class = AttendanceSerializer
    list_serializer_class = AttendanceListSerializer

    permission_classes = [IsAuthenticated,]

    filter_backends = [DjangoFilterBackend,]
    filterset_fields   = ['course', 'enrollment__student', 'enrollment__group', 'attendance_date'] # Filtros

    def _get_course(self, pk=None):
        if pk is not None:
            course = Course.objects.get(id=pk, state=True)
            if course:
                return course
            return None
        return None

    @action(detail=False, methods=['get'])
    def get_range_attendance_dates_by_course(self, request,):
        """
           Retorna una lista de las fechas de asistencia que tiene un curso para elegir en el reporte

            params --> course_id : int requerido

            ejemplo de url: /attendances/attendances/get_range_attendance_dates_by_course/?course_id=1

            ejemplo respuesta: {"dates": [ "2024-12-11", "2024-12-12", "2024-12-13", "2024-12-16" ]}
        """
        course_id = request.query_params.get('course_id', None)
        course = Course.objects.filter(id=course_id, state=True).first()

        if course:
            # obtener el rango de fechas de asistencias de un curso
            dates = models.Attendance.objects.filter(course=course, state=True).values_list('attendance_date', flat=True).distinct()
            # formatear cada fecha
            dates = [date.strftime('%Y-%m-%d') for date in dates]

            return Response({
            'dates': dates
        })
        
        return Response({
            'curso': 'No se existe el curso'
        })

    @action(detail=False, methods=['get'])
    def get_report_by_course(self, request,):
        """
           Retorna un reporte de asistencia de un curso, con el total de asistencias de cada estudiante

            params --> course_id : int                 requerido
            params --> start_date : date               requerido
            params --> end_date : date                 requerido
            params --> is_late : bool                  True por defecto
            params --> is_leave : bool                 True por defecto
            params --> three_late_is_an_absent : bool  False por defecto

            ejemplo de url: /attendances/attendances/get_report_by_course
                            /?course_id=1
                            &start_date=2024-12-11
                            &end_date=2024-12-16
                            &is_late=True
                            &is_leave=True  
                            &three_late_is_an_absent=True

            Retorna: 
            { "Report": {
                course,
                start_date,
                end_date,
                is_late,
                is_leave,
                three_late_is_an_absent,
                atendances: [
                    student,
                    total_attendances,
                ]
                } 
            {
        """
        course_id = request.query_params.get('course_id', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        is_late = request.query_params.get('is_late', True)
        is_leave = request.query_params.get('is_leave', True)
        three_late_is_an_absent = request.query_params.get('three_late_is_an_absent', False)

        query_params_data = {
            'course_id': course_id,
            'start_date': start_date,
            'end_date': end_date,
            'is_late': is_late,
            'is_leave': is_leave,
            'three_late_is_an_absent': three_late_is_an_absent
        }
        
        attendanceReportSerializer = AttendanceReportSerializer(data=query_params_data)

        if attendanceReportSerializer.is_valid():
            return Response({
                'Report': attendanceReportSerializer.data
            })
       
        return Response({
            'errors': attendanceReportSerializer.errors
        })
    
    def _get_hetatmap_from_course(self, course=None):
        if course is not None:

            attendances =  models.Attendance.objects.filter(
                state=True, 
                course=course,
            )
            dates = attendances.values_list('attendance_date', flat=True).distinct()

            heatmap_data = {}

            for date in dates:
                heatmap_data[date.strftime('%Y-%m-%d')] = attendances.filter(
                    attendance_date=date,
                    attendance_status__in=['PRESENT', 'LATE', 'LEAVE']
                ).count()

            return {
                'start_date': dates.first().strftime('%Y-%m-%d') if dates else '',
                'end_date': dates.last().strftime('%Y-%m-%d') if dates else '',
                'total_attendances': attendances.count(),
                'total_days': len(dates),
                'heatmap_data': heatmap_data
            }
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': {'course': 'El curso no existe'}
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_heatmap(self, request):
        """
            Retorna la información de todas las asistencias de un curso para el heatmap

            ejemplo de url: /attendances/attendances/get_attendances/?course_id=1
        """
        course_id = request.query_params.get('course_id', None)

        course = self._get_course(course_id)

        if course:
            # Obtén las asistencias del curso
            attendances_data = self._get_hetatmap_from_course(course)
        
            return Response(attendances_data)
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': {'course': 'El curso no existe'}
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self, pk=None, user=None):
        from apps.users.models import Roles

        if pk is None:
            if user.rol == Roles.TEACHER:
                return models.Attendance.objects.filter(course__teacher=user, state=True)
            if user.rol == Roles.STUDENT:
                return models.Attendance.objects.filter(enrollment__student=user, state=True)
            return models.Attendance.objects.filter(state=True)
        return models.Attendance.objects.filter(id=pk, state=True).first()
  
    def list(self, request):
        """
        Retorna una lista de todas las asistencias activas

        ejemplo de url: /attendances/attendances/
        """
        attendances = self.filter_queryset(self.get_queryset(user=request.user))
        page = self.paginate_queryset(attendances)  # Aplica la paginación
        serializer = self.list_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        """
        Crea una lista de asistencia con los datos enviados en el request

        metodo: POST

        ejemplo de url: /attendances/attendances/

        ejemplo de request: 
        [
            {
                "course": 1,
                "enrollment": 1,
                "attendance_date": "2024-12-11",
                "attendance_status": "PRESENT"
            },
            {
                "course": 1,
                "enrollment": 2,
                "attendance_date": "2024-12-11",
                "attendance_status": "PRESENT"
            }
        ]

        """
        serializer = self.list_serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message':'Asistencias registradas correctamente!'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message':'', 'error':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
            Retorna la información de una asistencia

            ejemplo de url: /attendances/attendances/1/
        """
        attendance = self.get_queryset(pk)
        if attendance:
            attendance_serializer = self.serializer_class(attendance)
            return Response(attendance_serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Asistencia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
       """
        Actualiza los datos de una asistencia

        metodo: PUT

        ejemplo de url: /attendances/attendances/1/
        """
       if self.get_queryset(pk):
            attendance_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)           
            if attendance_serializer.is_valid():
                attendance_serializer.save()
                return Response({
                    'message':'Asistencia actualizada correctamente!'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'', 'error':attendance_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)  

    def destroy(self, request, pk=None): 
        """
        Actualiza el estado de una asistencia a False

        ejemplo de url: /attendances/attendances/1/
        """      
        attendance = self.get_queryset(pk)      
        if attendance:
            attendance.state = False
            attendance.save()
            return Response({'message':'Asistencia eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe una Asistencia con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete_attendance_list(self, request):
        """
        Elimina una lista de asistencia de un curso en una fecha específica

        method: DELETE

        params --> course_id : int requerido
        params --> attendance_date : date requerido

        ejemplo de url: /attendances/attendances/delete_attendance_list/?course_id=1&attendance_date=2024-12-11
        """
        course_id = request.query_params.get('course_id')
        course = self._get_course(course_id)
        attendance_date = request.query_params.get('attendance_date')
       
        try:
            attendance_list = models.Attendance.objects.filter(
                course = course,
                attendance_date = attendance_date,
                state = True
            )
            if attendance_list:
                
                attendance_list.update(state=False)
                return Response(
                    {'message': 'Asistencias eliminadas correctamente!'},
                    status=status.HTTP_200_OK
                )
            return Response({'error': 'No existe una lista de asistencia con estos datos!'},)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
