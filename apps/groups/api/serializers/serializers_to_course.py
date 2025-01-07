from rest_framework import serializers

from apps.users.models import User
from apps.groups.models import *

class TeacherSerializerToCourse(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name',)

class SubjectSerializerToCourse(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'image')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'image': instance.image.url if instance.image != '' else '',
        }

class SchoolRoomSerializerToCourse(serializers.ModelSerializer):
    class Meta:        
        model = SchoolRoom
        fields = ('id', 'name',)

class DepartmentSerializerToCourse(serializers.ModelSerializer):
    class Meta:        
        model = Department
        fields = ('id', 'name',)

class PeriodSerializerToCourse(serializers.ModelSerializer):
    class Meta:        
        model = Period
        fields = ('id', 'name',)
