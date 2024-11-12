from rest_framework import serializers

from apps.groups.models import ClassGroup

class ClassGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClassGroup
        exclude = ('state','created_date','modified_date','deleted_date')

    def validate_name(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un Nombre")
        return value

    def validate_teacher(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un Docente")
        return value
    
    def validate_period(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar un Periodo")
        return value

    def validate_subject(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar una Materia")
        return value
    
    def validate_school_room(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Debe ingresar una Aula")
        return value

    def validate(self, data):
        if 'name' not in data.keys():
            raise serializers.ValidationError({
                "name": "Debe ingresar un nombre."
            })
        
        if 'teacher' not in data.keys():
            raise serializers.ValidationError({
                "teacher": "Debe ingresar un Docente."            
            })
        
        if 'subject' not in data.keys():
            raise serializers.ValidationError({
                "name": "Debe ingresar una Materia."
            })
        
        if 'period' not in data.keys():
            raise serializers.ValidationError({
                "period": "Debe ingresar un Periodo."            
            })
        
        if 'school_room' not in data.keys():
            raise serializers.ValidationError({
                "name": "Debe ingresar un Aula."
            })
        
        return data