from rest_framework import serializers

from apps.attendances.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'group', 'state')

    def validate_student(self, value):
        if value.rol != 'STUDENT':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de STUDENT")
        return value
    
    
    def to_representation(self,instance):
        return {
            'id': instance.id,           
            'student': instance.student.full_name if instance.student is not None else '',
            'group': instance.group.name if instance.group is not None else '',
        }

class EnrollmentRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        exclude = ('state','created_date','modified_date','deleted_date')