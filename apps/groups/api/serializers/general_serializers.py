import datetime
from rest_framework import serializers

from apps.groups.models import Subject, Departament, Period, SchoolRoom

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