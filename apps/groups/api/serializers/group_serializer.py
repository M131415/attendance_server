from rest_framework import serializers

from apps.groups.models import ClassGroup

class ClassGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassGroup
        exclude = ('state','created_date','modified_date','deleted_date')

    def validate_teacher(self, value):
        if value.rol != 'TEACHER':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de TEACHER")
        return value
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'name': instance.name,            
            'teacher': instance.teacher.full_name if instance.teacher is not None else '',
            'subject': instance.subject.name if instance.subject is not None else '',
            'period': instance.period.period if instance.period is not None else '',
            'school_room': instance.school_room.name if instance.school_room is not None else '',
        }

class ClassGroupRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassGroup
        exclude = ('state','created_date','modified_date','deleted_date')