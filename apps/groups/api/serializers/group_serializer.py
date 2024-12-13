from rest_framework import serializers

from apps.groups.models import Group, Course
from apps.attendances.models import Enrollment

# Serializador que se utiliza para crear una inscripcion junto a un grupo
class EnrollmentSerializerToGroup(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student']

    def validate_student(self, value):
        if value.rol != 'STUDENT':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de STUDENT")
        return value
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'student': instance.student.full_name
        }

# Serializador para mostrar una lista de cursos de un grupo
class CourseListSerializerToGroup(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','teacher','subject','school_room','department',)

    def to_representation(self,instance):
        return {
            'id': instance.id,
            'teacher': instance.teacher.full_name if instance.teacher is not None else '',            
            'subject': instance.subject.name if instance.subject is not None else '',
            'subject_image_url': instance.subject.image.url if instance.subject.image != '' else '',            
            'school_room': instance.school_room.name if instance.school_room is not None else '',
            'department': instance.department.name if instance.department is not None else '',            
        }

# Serializador para crear o recupera un grupo
class GroupSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializerToGroup(required=False, many=True)
    courses = CourseListSerializerToGroup(required=False, many=True)

    class Meta:
        model = Group
        fields = ('id','name','period','enrollments_count', 'courses_count','courses', 'enrollments')

    def create(self, validated_data):
        enrollments_data = validated_data.pop('enrollments')
        group = Group.objects.create(**validated_data)
        for schedule_data in enrollments_data:
            Enrollment.objects.create(group=group, **schedule_data)
        return group
    
    def to_representation(self,instance):
        course_serializer = CourseListSerializerToGroup(instance.courses, many=True)
        enrollment_serializer = EnrollmentSerializerToGroup(instance.enrollments, many=True, )
        return {
            'id': instance.id,
            'name': instance.name,            
            'period': instance.period.name,
            'enrollments_count': instance.enrollments_count,
            'courses_count': instance.courses_count,
            'courses': course_serializer.data,
            'enrollments': enrollment_serializer.data
        }

# Serializador para mostrar una lista de grupos      
class GroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id','name','period','enrollments_count', 'courses_count')
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'name': instance.name,            
            'period': instance.period.name,
            'enrollments_count': instance.enrollments_count,
            'courses_count': instance.courses_count
        }

# Serializador para actualizar un grupo
class GroupUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id','name','period',)
    