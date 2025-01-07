import datetime

from rest_framework import serializers

from apps.attendances.models import Enrollment
from apps.groups.models import Course, Schedule, Group

from apps.users.api.serializers.user_serializer import UserListSerializer
from apps.groups.api.serializers.serializers_to_course import *

# Serializador que se utiliza para crear un horario junto a un curso
class ScheduleSerializerToCourse(serializers.ModelSerializer):

    def validate_start_time(self, start_time):
        if start_time < datetime.time(hour=7):
            raise serializers.ValidationError("La Hora de Inicio no debe ser menor que las 7 am") 
        return start_time
    
    def validate_end_time(self, end_time):
        int_list = list(map(int, self.context['start_time'].split(':')))
        start_time = datetime.time(hour=int_list[0])
        
        if end_time > datetime.time(hour=20):
            raise serializers.ValidationError("La Hora de Fin no debe ser mayor que las 8 pm")
        elif end_time < start_time:
            raise serializers.ValidationError("La Hora de Fin no puede ser menor a la Hora de Inicio") 
        return end_time
    
    class Meta:
        model = Schedule
        fields = ['id', 'day_of_week', 'start_time', 'end_time']

# Serializador que se utiliza para visualizar la informacion de una inscripcion 
class EnrollmentSerializerToCourse(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student']
    
    def to_representation(self,instance):
        student_serializer = UserListSerializer(instance.student)
        return {
            'id': instance.id,
            'student': student_serializer.data
        }

# Serializador que se utiliza solo para leer la informacion del grupo
class GroupSerializerToCourse(serializers.ModelSerializer,):
    enrollments = EnrollmentSerializerToCourse(required=False, many=True)

    class Meta:
        model = Group
        fields = ('id','name','enrollments_count', 'enrollments')
    
    def to_representation(self,instance):
        # Filtrar inscripciones con estado en True
        active_enrollments = instance.enrollments.filter(state=True)

        enrollment_serializer = EnrollmentSerializerToCourse(active_enrollments, many=True,)
        return {
            'id': instance.id,
            'name': instance.name,            
            'enrollments_count': instance.enrollments_count,
            'enrollments': enrollment_serializer.data
        }

# Selializador para crear o recuperar un curso
class CourseSerializer(serializers.ModelSerializer):

    schedules = ScheduleSerializerToCourse(many=True, required=False)

    class Meta:
        model = Course
        fields = ('id','teacher','group','subject','school_room','department','period','schedules')

    def validate_group(self, group):
        try:
            # Intenta convertir el periodo del contexto a un entero
            period = int(self.context.get('period'))
        except (ValueError, TypeError):
            raise serializers.ValidationError("El periodo proporcionado en el contexto no es válido.")

        if not period:
            raise serializers.ValidationError("El periodo no fue proporcionado en el contexto.")
        
        # Verifica que el periodo del grupo coincida con el periodo del contexto
        if group.period.id != period:
            raise serializers.ValidationError("El periodo del Grupo debe pertenecer al mismo que el  del Curso.")
        
        return group


    def create(self, validated_data):
        if 'schedules' not in validated_data.keys():
            course = Course.objects.create(**validated_data)
            return course
        
        schedules_data = validated_data.pop('schedules')
        course = Course.objects.create(**validated_data)
        for schedule_data in schedules_data:
            Schedule.objects.create(course=course, **schedule_data)
        return course
    
    def to_representation(self,instance):
        # Filtrar horarios con estado en True
        active_schedules = instance.schedules.filter(state=True)

        schedules_serializer = ScheduleSerializerToCourse(active_schedules, many=True)
        group_serializer = GroupSerializerToCourse(instance.group)
        teacher_serializer = TeacherSerializerToCourse(instance.teacher)
        subject_serializer = SubjectSerializerToCourse(instance.subject)
        school_room_serializer = SchoolRoomSerializerToCourse(instance.school_room)
        department_serializer = DepartmentSerializerToCourse(instance.department)
        period_serializer = PeriodSerializerToCourse(instance.period)
        
        return {
            'id': instance.id,
            'teacher': teacher_serializer.data,            
            'subject': subject_serializer.data,
            'school_room': school_room_serializer.data,
            'department': department_serializer.data,            
            'period': period_serializer.data,
            'schedules': schedules_serializer.data,
            'group': group_serializer.data,
        }

# Serializador para mostrar una lista de curso 
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','teacher','group','subject','school_room','department','period',)

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'teacher': instance.teacher.full_name if instance.teacher is not None else '',            
            'group': instance.group.name if instance.group is not None else '',
            'subject': instance.subject.short_name if instance.subject is not None else '',
            'subject_image_url': instance.subject.image.url if instance.subject.image != '' else '',            
            'school_room': instance.school_room.name if instance.school_room is not None else '',
            'department': instance.department.name if instance.department is not None else '',            
            'period': instance.period.name if instance.period is not None else '',
        }

# Serializador para actualizar un curso
class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','teacher','group','subject','school_room','department','period', )
        
    def validate_teacher(self, value):
        if value.rol != 'TEACHER':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de TEACHER")
        return value