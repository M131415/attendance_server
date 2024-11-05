from django.contrib import admin
from apps.groups.models import *

# Register your models here.
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'teacher',
        'subject',
        'period',
        'school_room',
    )

class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'day_of_week',
        'start_time',
        'end_time',
    )

admin.site.register(ClassGroup, ClassGroupAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Subject)
admin.site.register(Departament)
admin.site.register(Period)
admin.site.register(SchoolRoom)