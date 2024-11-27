from django.contrib import admin
from apps.attendances.models import *

# Register your models here.
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'group',
    )
    
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'attendance_date',
        'enrollment',
        'attendance_status',
        'observation',
    )

admin.site.register(Enrollments, EnrollmentAdmin)
admin.site.register(Attendances, AttendanceAdmin)