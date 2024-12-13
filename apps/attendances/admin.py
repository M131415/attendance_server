from django.contrib import admin
from apps.attendances.models import *

# Register your models here.
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'group',
        'state',
    )
    
    list_filter = (
        'student',
        'group',
    )

class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'attendance_date',
        'course',
        'enrollment',
        'attendance_status',
        'observation',
        'state'
    )

    list_filter = (
        'attendance_date',
        'course',
        'enrollment',
        'attendance_status',
    )

admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Attendance, AttendanceAdmin)