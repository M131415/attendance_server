from rest_framework import serializers

from apps.attendances.models import Enrollments

class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollments
        exclude = ('state','created_date','modified_date','deleted_date')

    def validate_student(self, value):
        if value.rol != 'STUDENT':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de STUDENT")
        return value
    
    def validate(self, data):
        if 'grupo' not in data.keys():
            raise serializers.ValidationError({
                "grupo": "Debe ingresar un grupo"
            })
        return data
    
    def to_representation(self,instance):
        return {
            'id': instance.id,           
            'student': instance.student.full_name if instance.student is not None else '',
            'group': instance.group.name if instance.group is not None else '',
        }

class EnrollmentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollments
        exclude = ('state','created_date','modified_date','deleted_date')