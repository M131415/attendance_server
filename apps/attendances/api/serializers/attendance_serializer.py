from rest_framework import serializers

from apps.attendances.models import Attendances

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendances
        exclude = ('state','created_date','modified_date','deleted_date')
    
    def validate(self, data):
        if 'course' not in data.keys():
            raise serializers.ValidationError({
                "course": "Debe ingresar un curso"
            })
        elif data['enrollment'].group != data['course'].group:
            raise serializers.ValidationError({
                "grupo": "El grupo se inscripción no coincide con el del curso"
            })
        
        print(data)
        return data
    
    def to_representation(self,instance):
        return {
            'id': instance.id,           
            'enrollment':  {
                'student': instance.enrollment.student.full_name,
                'group': instance.enrollment.group.name
            },
            'course':  {
                'teacher': instance.course.teacher.full_name,
                'subject': instance.course.subject.name,
            },
            'observation': instance.observation if instance.observation is not None else '',
            'attendance_status': instance.attendance_status, 
            'attendance_date': instance.attendance_date, 
        }