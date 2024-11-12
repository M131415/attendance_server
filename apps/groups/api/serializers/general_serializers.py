from rest_framework import serializers

from apps.groups.models import Subject, Departament, Period, SchoolRoom

class SubjecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields =  ('id', 'name')

class SubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'name': instance['name'],
        }

class DepartamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields =  ('id', 'name')

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields =  ('start_date', 'end_date')

class SchoolRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolRoom
        fields =  ('id', 'name')