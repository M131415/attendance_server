from rest_framework import serializers

from apps.users.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate_rol(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un rol STUDENT")
        elif value != 'STUDENT':
            raise serializers.ValidationError("Debe ingresar un rol STUDENT")
        return value
    
    def create(self,validated_data):
        student = User(**validated_data)
        student.set_password(validated_data['password'])
        student.save()
        return student

    def validate(self, data):
        if 'rol' not in data.keys():
            raise serializers.ValidationError({
                "rol": "Debe ingresar un rol STUDENT"
            })
        return data

class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name',)


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
            'username': instance['username'],
            'email': instance['email'],
            
        }
