from rest_framework import serializers

from apps.groups.models import Course, Schedule, Group
from apps.attendances.models import Enrollment

from apps.users.api.serializers.user_serializer import UserListSerializer

# Serializador que se utiliza para crear un horario junto a un curso
class ScheduleSerializerToCourse(serializers.ModelSerializer):
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
        fields = ('id','name','period','enrollments_count', 'enrollments')
    
    def to_representation(self,instance):
        enrollment_serializer = EnrollmentSerializerToCourse(instance.enrollments, many=True, )
        return {
            'id': instance.id,
            'name': instance.name,            
            'period': instance.period.name,
            'enrollments_count': instance.enrollments_count,
            'enrollments': enrollment_serializer.data
        }

# Selializador para crear o recuperar un curso
class CourseSerializer(serializers.ModelSerializer):

    schedules = ScheduleSerializerToCourse(many=True, required=False)

    class Meta:
        model = Course
        fields = ('id','teacher','group','subject','school_room','department','period','schedules')

    def create(self, validated_data):
        schedules_data = validated_data.pop('schedules')
        course = Course.objects.create(**validated_data)
        for schedule_data in schedules_data:
            Schedule.objects.create(course=course, **schedule_data)
        return course
    
    def to_representation(self,instance):
        schedules_serializer = ScheduleSerializerToCourse(instance.schedules, many=True)
        group_serializer = GroupSerializerToCourse(instance.group)
        return {
            'id': instance.id,
            'teacher': instance.teacher.full_name if instance.teacher is not None else '',            
            'subject': instance.subject.name if instance.subject is not None else '',
            'subject_image_url': instance.subject.image.url if instance.subject.image != '' else '',            
            'school_room': instance.school_room.name if instance.school_room is not None else '',
            'department': instance.department.name if instance.department is not None else '',            
            'period': instance.period.name if instance.period is not None else '',
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
            'subject': instance.subject.name if instance.subject is not None else '',
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