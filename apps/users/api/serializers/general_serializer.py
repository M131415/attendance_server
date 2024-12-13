from rest_framework import serializers

from apps.users.models import Career, TeacherProfile, StudentProfile

# Serializador de Carrera
class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ('id', 'code', 'name', 'short_name', 'specialty',)

# Serializador del perfil del docente
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ('degree',)

    def validate_degree(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("El Grado Académico no puede estar vacío")
        return value
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'degree': instance.degree,
        }
    
# Serializador del perfil del estudiante
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('career',)

    def validate_career(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("La carrera no puede estar vacía")
        return value
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'career': instance.career.name,
        }
    