import datetime

from rest_framework import serializers

from apps.groups.models import Subject, Department, Period, SchoolRoom, Schedule

class SubjecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields =  ('id','code', 'name', 'short_name', 'image')
    
    def to_representation(self,instance):
        return {
            'id': instance.id,    
            'code': instance.code, 
            'name': instance.name, 
            'short_name': instance.short_name,
            'semester': instance.semester,
            'image': instance.image.url if instance.image != '' else '',
        }

class DepartamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields =  ('id', 'name')

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields =  ('id','code', 'name', 'start_date', 'end_date')

    def validate_end_date(self, end_date):
        int_list = list(map(int, self.context['start_date'].split('-')))
        
        start_date = datetime.date(int_list[0], int_list[1], int_list[2])
        
        if end_date < start_date:
            raise serializers.ValidationError("La Fecha de Fin debe ser mayor que la Fecha de Inicio") 
        return end_date
    
    def validate(self, data):
        if 'name' not in data.keys():
            raise serializers.ValidationError({
                "name": "Debe ingresar un nombre del periodo"
            })
        return data

class SchoolRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolRoom
        fields =  ('id', 'name')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields =  ('id', 'course', 'day_of_week', 'start_time', 'end_time')

class ScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields =  ('id', 'course', 'day_of_week', 'start_time', 'end_time')
    
    def to_representation(self,instance):
        from apps.groups.api.serializers.course_serializer import CourseListSerializer

        course_serializer = CourseListSerializer(instance.course)

        return {
            'id': instance.id,
            'course': course_serializer.data,         
            'day_of_week': instance.day_of_week, 
            'start_time': instance.start_time, 
            'end_time': instance.end_time, 
        }