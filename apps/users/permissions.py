from rest_framework.permissions import BasePermission
from apps.users.models import Roles

class IsAdminOrTeacherUser(BasePermission):
    """
    Permite el acceso a los usuarios que sean administradores o maestros.
    """
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.rol == Roles.TEACHER
    
class IsAdminOrStudentUser(BasePermission):
    """
    Permite el acceso a los usuarios que sean administradores o estudiantes.
    """
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.rol == Roles.STUDENT