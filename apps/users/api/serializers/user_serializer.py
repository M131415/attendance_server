from rest_framework import serializers


from apps.users.models import User
from apps.users.models import Roles
from apps.users.api.serializers.general_serializer import TeacherProfileSerializer, StudentProfileSerializer

# Serializadores para mostrar la informacion de cada usuario basado en su rol
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'rol',)

class TeacherSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'rol', 'teacher_profile')

class StudentSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'rol', 'student_profile')

# Serializador para crear un usuario
class UserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=False)
    student_profile = StudentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'last_name', 'rol', 'password', 'teacher_profile', 'student_profile')
    
    def validate_rol(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un rol TEACHER, STUDENT o ADMIN")
        return value
    
    def validate(self, data):
        if data['rol'] == Roles.TEACHER:
            if 'teacher_profile' not in data.keys():
                raise serializers.ValidationError({
                    "teacher_profile": "Debe ingresar un Perfil del Docente"
                })
        elif data['rol'] == Roles.STUDENT:
            if 'student_profile' not in data.keys():
                raise serializers.ValidationError({
                    "student_profile": "Debe ingresar un Perfil del Estudiante"
                })
        return data
    
    def create(self,validated_data):
        # Extraer información de los perfiles antes de crear el usuario
        teacher_data = validated_data.pop('teacher_profile', None)
        student_data = validated_data.pop('student_profile', None)
        rol = validated_data.get('rol')

        # Crear el usuario
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Encriptar la contraseña
        if rol == Roles.ADMIN:
            user.is_superuser = True
        user.save()

        # Crear el perfil correspondiente si aplica
        if rol == Roles.TEACHER and teacher_data:
            TeacherProfileSerializer.Meta.model.objects.create(user=user, **teacher_data)
        elif rol == Roles.STUDENT and student_data:
            StudentProfileSerializer.Meta.model.objects.create(user=user, **student_data)

        return user
    
    def to_representation(self,instance):
        if instance.rol == Roles.ADMIN:
            admin_serializer = AdminSerializer(instance)
            return admin_serializer.data
        elif instance.rol == Roles.TEACHER:
            admin_serializer = TeacherSerializer(instance)
            return admin_serializer.data
        elif instance.rol == Roles.STUDENT:
            admin_serializer = StudentSerializer(instance)
            return admin_serializer.data

# Serializador para Actualizar un usuario en base a su rol
class UpdateUserSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=False)
    student_profile = StudentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'teacher_profile', 'student_profile')

    def update(self, instance, validated_data):
        teacher_data = validated_data.pop('teacher_profile', None)
        student_data = validated_data.pop('student_profile', None)

        # Actualizar el usuario
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Actualizar el perfil correspondiente
        if instance.rol == Roles.TEACHER and teacher_data:
            teacher_profile = instance.teacher_profile
            for key, value in teacher_data.items():
                setattr(teacher_profile, key, value)
            teacher_profile.save()

        if instance.rol == Roles.STUDENT and student_data:
            student_profile = instance.student_profile
            for key, value in student_data.items():
                setattr(student_profile, key, value)
            student_profile.save()

        return instance

# Serializador para reestablecer una contraseña de usuario 
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data
    
# Serializador para mostrar la lista de usuarios
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name',]

   
