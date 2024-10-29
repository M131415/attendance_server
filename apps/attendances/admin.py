from django.contrib import admin
from apps.attendances.models import *
# Register your models here.

admin.site.register([Enrollments, Attendances])