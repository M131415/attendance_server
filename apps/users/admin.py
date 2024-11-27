from django.contrib import admin
from apps.users.models import User, StudentProfile, TeacherProfile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'full_name',
        'rol',
        'is_active',
    )
    
    list_filter = (
        'rol',
        "is_active"
    )

    def save_model(self, request, user, form, change):
        user.set_password(user.password)
        super().save_model(request, user, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)