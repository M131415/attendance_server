from rest_framework import serializers

from apps.groups.models import Course

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        exclude = ('state','created_date','modified_date','deleted_date')

    def validate_teacher(self, value):
        if value.rol != 'TEACHER':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de TEACHER")
        return value
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'teacher': instance.teacher.full_name if instance.teacher is not None else '',            
            'group': instance.group.name if instance.group is not None else '',
            'subject': instance.subject.name if instance.subject is not None else '',            
            'school_room': instance.school_room.name if instance.school_room is not None else '',
            'departament': instance.departament.name if instance.departament is not None else '',            
            'period': instance.period.period if instance.period is not None else '',
        }
    
class CourseRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        exclude = ('state','created_date','modified_date','deleted_date')
