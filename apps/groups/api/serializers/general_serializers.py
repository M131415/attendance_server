import datetime
from rest_framework import serializers

from apps.groups.models import Subject, Departament, Period, SchoolRoom, Schedule, Group

class SubjecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields =  ('id', 'name')

class DepartamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields =  ('id', 'name')

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields =  ('id', 'start_date', 'end_date')

    def validate_end_date(self, end_date):
        int_list = list(map(int, self.context['start_date'].split('-')))
        
        start_date = datetime.date(int_list[0], int_list[1], int_list[2])
        
        if end_date < start_date:
            raise serializers.ValidationError("La Fecha de Fin debe ser mayor que la Fecha de Inicio") 
        return end_date

class SchoolRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolRoom
        fields =  ('id', 'name')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields =  ('id', 'course', 'day_of_week', 'start_time', 'end_time')

    def validate_start_time(self, start_time):
        if start_time < datetime.time(hour=7):
            raise serializers.ValidationError("La Hora de Inicio no debe ser menor que las 7 am") 
        return start_time
    
    def validate_end_time(self, end_time):
        int_list = list(map(int, self.context['start_time'].split(':')))
        start_time = datetime.time(hour=int_list[0])
        
        if end_time > datetime.time(hour=20):
            raise serializers.ValidationError("La Hora de Fin no debe ser mayor que las 8 pm")
        elif end_time < start_time:
            raise serializers.ValidationError("La Hora de Fin no puede ser menor a la Hora de Inicio") 
        return end_time

    def validate(self, data):
        if 'course' not in data.keys():
            raise serializers.ValidationError({
                "course": "Debe ingresar un curso"
            })
        return data
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'course': {
                'teacher': instance.course.teacher.full_name,
                'subject': instance.course.subject.name,
            },         
            'day_of_week': instance.day_of_week, 
            'start_time': instance.start_time, 
            'end_time': instance.end_time, 
        }

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id','name','period')
    
    def to_representation(self,instance):
        return {
            'id': instance.id,
            'name': instance.name,            
            'period': instance.period.period if instance.period is not None else '',
        }
