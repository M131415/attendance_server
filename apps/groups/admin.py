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
        'course',
        'day_of_week'
    )

admin.site.register(Group, GroupAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(Period)
admin.site.register(SchoolRoom)