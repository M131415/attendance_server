from django.contrib import admin
from apps.users.models import User, StudentProfile, TeacherProfile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'name',
        'last_name',
        'rol',
    )

    def save_model(self, request, user, form, change):
        if not change:  # Para cuando se está creando un usuario nuevo
            user.set_password(user.password)
        super().save_model(request, user, form, change)

admin.site.register(User, UserAdmin)
admin.site.register([StudentProfile, TeacherProfile])