from rest_framework import serializers

from apps.users.models import User

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate_rol(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un rol TEACHER")
        elif value != 'TEACHER':
            raise serializers.ValidationError("Debe ingresar un rol TEACHER")
        return value
    
    def create(self,validated_data):
        teacher = User(**validated_data)
        teacher.set_password(validated_data['password'])
        teacher.save()
        return teacher
    
    def validate(self, data):
        if 'rol' not in data.keys():
            raise serializers.ValidationError({
                "rol": "Debe ingresar un rol TEACHER"
            })
        return data


class UpdateTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name',)

  
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data

class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'last_name': instance['last_name'],
            'username': instance['username'],
            'email': instance['email'],
        }
