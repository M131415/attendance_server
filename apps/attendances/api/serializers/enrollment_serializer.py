from rest_framework import serializers

from apps.attendances.models import Enrollment

# Serializador solo para mostrar una lista de Inscripciones
class EnrollmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'group', 'state')

    def validate_student(self, value):
        if value.rol != 'STUDENT':
            raise serializers.ValidationError("Solo se admiten usuarios con el Rol de STUDENT")
        return value
    
    
    def to_representation(self,instance):
        from apps.groups.api.serializers.group_serializer import GroupListSerializer
        group_serializer = GroupListSerializer(instance.group)
        return {
            'id': instance.id,
            'student': instance.student.full_name if instance.student is not None else '',
            'group': group_serializer.data if instance.group is not None else '',
        }
# Serialidor para recuperar o crear una inscripcion
class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        exclude = ('state','created_date','modified_date','deleted_date')