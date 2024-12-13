from rest_framework import serializers

from apps.attendances.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('enrollment', 'course', 'observation', 'attendance_date', 'attendance_status')
    
    def to_representation(self,instance):
        return {
            'id': instance.id,           
            'enrollment': instance.enrollment.id,
            'course': instance.course.id,
            'observation': instance.observation if instance.observation is not None else '',
            'attendance_status': instance.attendance_status, 
            'attendance_date': instance.attendance_date, 
        }
    
class TakeAttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('id', 'enrollment', 'course', 'observation', 'attendance_date', 'attendance_status')