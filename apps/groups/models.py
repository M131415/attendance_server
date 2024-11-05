from django.conf import settings
from django.db import models

from apps.base.models import BaseModel

# Materia 
class Subject(BaseModel):
    name = models.CharField("Nombre de la materia", max_length=256, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        db_table = 'subject'

    def __str__(self):
        return f'{self.name}'

# Departamento
class Departament(BaseModel):
    name = models.CharField("Nombre del departamento", max_length=128, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        db_table = 'departament'

    def __str__(self):
        return f'{self.name}'

# Periodo
class Period(BaseModel):
    start_date = models.DateField("Fecha de inicio", null=False, blank=False, unique=True)
    end_date = models.DateField("Fecha de fin", null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        db_table = 'period'

    def __str__(self):
        return f'{self.start_date}/{self.end_date}'
# Aula
class SchoolRoom(BaseModel):
    name = models.CharField("Nombre del Aula", max_length=256, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        db_table = 'school_room'

    def __str__(self):
        return f'{self.name}'

# Grupo de Clases
class ClassGroup(BaseModel):
    name = models.CharField("Nombre del grupo", max_length=256, null=False, blank=False)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Docente",)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Materia")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Periodo")
    school_room = models.ForeignKey(SchoolRoom, on_delete=models.CASCADE, verbose_name="Aula")

    class Meta:
        verbose_name = 'Grupo de clases'
        verbose_name_plural = 'Grupos de clases'
        db_table = 'class_group'

    def __str__(self):
        return f'{self.name} docente: {self.teacher}'

# Dias de la Semana
class DayOfWeek(models.TextChoices):
    MONDAY    = "MONDAY", "Monday"
    TUESDAY   = "TUESDAY", "Tuesday"
    WEDNESDAY = "WEDNESDAY", "Wednesday"
    THURSDAY  = "THURSDAY", "Thursday"
    FRIDAY    = "FRIDAY", "Friday",
    SATURDAY  = 'SATURDAY', 'Saturday'
    SUNDAY    = "SUNDAY", "Sunday"

# Horario de Grupo de clases
class Schedule(BaseModel):
    group = models.ForeignKey(ClassGroup, verbose_name=("Grupo de clases"), on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=20, choices=DayOfWeek.choices, default=DayOfWeek.MONDAY
    )
    start_time = models.TimeField("Hora de inicio", null=False, blank=False, )
    end_time = models.TimeField("Hora de fin", null=False, blank=False, )

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        db_table = 'schedule'

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} : {self.end_time}'
