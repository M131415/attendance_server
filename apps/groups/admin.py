from django.contrib import admin
from apps.groups.models import *

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'period',
        'enrollments_count',
        'courses_count',
    )

class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'teacher',
        'group',
        'subject',
        'school_room',
        'department',
        'period',
    )

class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'course',
        'day_of_week',
        'start_time',
        'end_time',
    )

    list_filter = (
        'day_of_week',
    )

class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
        'short_name',
        'semester',
        'career',
    )
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )

class PeriodAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'code',
        'name',
        'start_date',
        'end_date',
    )

class SchoolRoomAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    
admin.site.register(Group, GroupAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(SchoolRoom, SchoolRoomAdmin)