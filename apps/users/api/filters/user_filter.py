import django_filters

from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    
    class Meta:
        model = User
        fields = {
            'rol': ['exact'],
            'is_active': ['exact'],
            'student_profile__career': ['exact']
        }
            
        