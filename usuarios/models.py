from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords


class UserManager(BaseUserManager):
    def _create_user(self, email, full_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email = email,
            full_name = full_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    full_name = models.CharField('Nombre Completo', max_length = 255, blank = True, null = True)
    image = models.ImageField('Imagen de perfil', upload_to='profile/', max_length=255, null=True, blank = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.full_name}'

class Docente(User):
    carrera = models.CharField('Carrera')

class Estudiante(User):
    contro_no = models.CharField('No de control')