from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.conf import settings
from apps.base.models import BaseModel

class UserManager(BaseUserManager):
    def _create_user(self, username, name,last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            name = name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, name, last_name, password=None, **extra_fields):
        return self._create_user(username, name,last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, name,last_name, password=None, **extra_fields):
        return self._create_user(username, name,last_name, password, True, True, **extra_fields)
    
# Roles de usuario
class Roles(models.TextChoices):
    ADMIN   = "ADMIN", "Admin"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"

class User(AbstractBaseUser, PermissionsMixin):
        
    username = models.CharField('Nombre de Usuario', max_length = 255, unique = True)
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True, null=False, blank=False)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    image = models.ImageField('Imagen de perfil', upload_to='perfil/', max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField("Fecha de Incorporación", default=timezone.now)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    rol = models.CharField(
        max_length=30, choices=Roles.choices, 
        default=Roles.ADMIN, null=False, blank=False,
    )
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'auth_user'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name','last_name',]

    def __str__(self):
        return f'{self.name} {self.last_name} {self.rol}'

class TeacherProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    carrera = models.CharField('Carrera', max_length=128)

    def __str__(self):
        return f'{self.user.name} {self.user.last_name}'
    
    class Meta:
        verbose_name = 'Perfil de Docente'
        verbose_name_plural = 'Perfiles de Docentes'
        db_table = 'teacher_profile'

class StudentProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    control_no = models.CharField('No de control', max_length=128)

    def __str__(self):
        return f'{self.user.name} {self.user.last_name}'
    
    class Meta:
        verbose_name = 'Perfil de Estudiante'
        verbose_name_plural = 'Perfiles de Estudiantes'
        db_table = 'student_profile'

# Signal Cuando se crea un usuario
""" @receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.rol == 'STUDENT':
            StudentProfile.objects.create(user=instance, control_no = instance.username)
        elif instance.rol == 'TEACHER':
            TeacherProfile.objects.create(user=instance)
 """
# todo Signal Cuando se Actializa o guarda un usuario
