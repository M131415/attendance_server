import datetime
from rest_framework import serializers

from apps.groups.api.serializers.course_serializer import EnrollmentSerializerToCourse
from apps.attendances.models import Attendance, Enrollment
from apps.groups.api.serializers.course_serializer import CourseListSerializer
from apps.groups.models import Course

#Serializador para recuperar, actualizar o crear una asistencia
class AttendanceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('id', 'enrollment', 'course', 'observation', 'attendance_date', 'attendance_status')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self,instance):
        return {
            'id': instance.id,           
            'enrollment': {
                'id': instance.enrollment.id,
                'student': {
                    'full_name': instance.enrollment.student.full_name,
                    'username': instance.enrollment.student.username,
                    'image': instance.enrollment.student.image.url if instance.enrollment.student.image else '',
                },
                'group': {
                    'name': instance.enrollment.group.name,
                }
            },
            'course': '',
            'observation': instance.observation if instance.observation is not None else '',
            'attendance_status': instance.attendance_status, 
            'attendance_date': instance.attendance_date, 
        }


#Serializador para recuperar, actualizar o crear una asistencia
class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('id', 'enrollment', 'course', 'observation', 'attendance_date', 'attendance_status')

    def validate(self, data):
        attendance_date = data['attendance_date']
        course = data['course']

        current_day_of_week = attendance_date.strftime("%A").upper()
        day_of_week_list = tuple(course.schedules.values_list('day_of_week', flat=True))
        
        if current_day_of_week not in day_of_week_list:
            raise serializers.ValidationError({
                "attendance_date": f"No puede tomar asistencia hoy {current_day_of_week}, este dia no esta en el horario del curso"
            })
        
        return data
    
    def to_representation(self,instance):
        return {
            'id': instance.id,           
            'enrollment': {
                'id': instance.enrollment.id,
                'student': {
                    'id': instance.enrollment.student.id,
                    'full_name': instance.enrollment.student.full_name,
                    'username': instance.enrollment.student.username,
                    'image': instance.enrollment.student.image.url if instance.enrollment.student.image else '',
                },
            },
            'course': instance.course.id,
            'observation': instance.observation if instance.observation is not None else '',
            'attendance_status': instance.attendance_status, 
            'attendance_date': instance.attendance_date, 
        }
    
class AttendanceReportSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_late = serializers.BooleanField()
    is_leave = serializers.BooleanField()
    three_late_is_an_absent = serializers.BooleanField()

    def validate_course_id(self, data):
        if data is None:
            raise serializers.ValidationError("El campo curso es requerido")
        return data
    
    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        
        if start_date > end_date:
            raise serializers.ValidationError({
                "start_date": "La fecha de inicio no puede ser mayor a la fecha de fin"
            })
        
        return data
    
    def get_attendances_with_enrollments(self, course, start_date, end_date, is_late, is_leave, three_late_is_an_absent):
        enrollments = Enrollment.objects.filter(group=course.group, state=True)

        attendancesByEnrollments = []
        attendance_status = ['PRESENT']
        
        if is_late:
            attendance_status.append('LATE')
        if is_leave:
            attendance_status.append('LEAVE')
        
        for enrollment in enrollments:
            # Obtener el total de asistencias de la inscripción del estudiante
            attendancesByEnrollment = Attendance.objects.filter(
                state=True,
                course=course,
                enrollment=enrollment,
                attendance_date__range=[start_date, end_date],
                attendance_status__in=attendance_status
            ).count()
            # Si es verdadero el valor de la asistencia se resta 1 por cada 3 llegadas tarde
            if is_late and three_late_is_an_absent:
                late_count = Attendance.objects.filter(
                    state=True,
                    course=course,
                    enrollment=enrollment,
                    attendance_date__range=[start_date, end_date],
                    attendance_status='LATE'
                ).count()
                attendancesByEnrollment -= late_count // 3

            # Serializar los datos del estudiante
            student_data = {
                'student': {
                    'id': enrollment.student.id,
                    'full_name': enrollment.student.full_name,
                    'username': enrollment.student.username,
                    'image': enrollment.student.image.url if enrollment.student.image else '',
                },
                'total_attendances': attendancesByEnrollment
            }
            attendancesByEnrollments.append(student_data)

        return attendancesByEnrollments
    
    def to_representation(self, instance):
        course = Course.objects.filter(id=instance['course_id'], state=True).first()
        
        if course:
            course_serializer = CourseListSerializer(course)
            start_date = instance['start_date']
            end_date = instance['end_date']
            is_late = instance['is_late']
            is_leave = instance['is_leave']
            three_late_is_an_absent = instance['three_late_is_an_absent']

            attendancesByEnrollments = self.get_attendances_with_enrollments(
                course=course,
                start_date=start_date,
                end_date=end_date,
                is_late=is_late,
                is_leave=is_leave,
                three_late_is_an_absent=three_late_is_an_absent
            )
            
            # attendanceSerializer = AttendanceSerializer(attendances, many=True)
            return {
                'course': course_serializer.data,
                'start_date': start_date,
                'end_date': end_date,
                'is_late': is_late,
                'is_leave': is_leave,
                'three_late_is_an_absent': three_late_is_an_absent,
                'atendances': attendancesByEnrollments,
            }
        else:
            raise serializers.ValidationError({
                "course": "El curso no existe"
            })
        

# Serializador para crear, recuperar, actualizar o eliminar una lista de asistencia de un curso
class TakeAttendancesCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField(required=False)
    attendance_date = serializers.DateField(required=False)
    attendance_list = AttendanceSerializer(many=True, required=False)

    def get_course(self, pk=None):
        if pk is not None:
            course = Course.objects.filter(id=pk, state=True).first()
            if course:
                return course
            raise serializers.ValidationError({"course_id": "No existe un curso con este id"})   
        raise serializers.ValidationError({"course_id": "El id del curso es requerido"})
  
    def to_representation(self, instance):
        course = self.get_course(instance['course_id'])
        attendance_date = instance['attendance_date']

        attendances = Attendance.objects.filter(
            course=course,
            attendance_date=attendance_date,
            state=True
        )

        serializer = AttendanceSerializer(attendances, many=True)
        
        return {
            'course_id': course.id,
            'attendance_date': attendance_date,
            'attendance_list': serializer.data
        }

    def create(self, validated_data):
        course = self.get_course(validated_data['course_id'])
        attendance_date = validated_data['attendance_date']
        attendances = validated_data['attendance_list']
        
        for attendance in attendances:
            attendance['course'] = course
            attendance['attendance_date'] = attendance_date
            Attendance.objects.create(**attendance)
        return validated_data
