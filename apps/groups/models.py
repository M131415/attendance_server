from django.conf import settings
from django.db import models

from apps.base.models import BaseModel

# 1. Materia 
class Subject(BaseModel):
    name = models.CharField("Nombre de la materia", max_length=256, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        db_table = 'subject'

    def __str__(self):
        return f'{self.name}'

# 2. Departamento
class Departament(BaseModel):
    name = models.CharField("Nombre del departamento", max_length=128, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        db_table = 'departament'

    def __str__(self):
        return f'{self.name}'

# 3. Periodo
class Period(BaseModel):
    start_date = models.DateField("Fecha de inicio", null=False, blank=False,)
    end_date = models.DateField("Fecha de fin", null=False, blank=False,)

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        db_table = 'period'

    @property
    def period(self):
        return f"{self.start_date}/{self.end_date}"

    def __str__(self):
        return f'{self.period}'
# 4. Aula
class SchoolRoom(BaseModel):
    name = models.CharField("Nombre del Aula", max_length=256, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        db_table = 'school_room'

    def __str__(self):
        return f'{self.name}'

# 5. Grupo
class Group(BaseModel):
    name = models.CharField("Nombre del grupo", max_length=256, null=False, blank=False)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Periodo", null=False, blank=False)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        db_table = 'group'

    def __str__(self):
        return f'{self.name}'

# 6. Curso
class Course(BaseModel):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Docente", null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Grupo", null=False, blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Materia", null=False, blank=False)
    school_room = models.ForeignKey(SchoolRoom, on_delete=models.CASCADE, verbose_name="Aula", null=False, blank=False)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE, verbose_name="Departamento", null=False, blank=False)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Periodo", null=False, blank=False)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos' 
        db_table = 'course'

        # Evita que un curso se repita
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'group', 'subject', 'period'], 
                condition=models.Q(state=True),
                name='unique_course'
            )
        ]

    def __str__(self):
        return f'{self.subject} docente: {self.teacher}'
    
# Dias de la Semana
class DayOfWeek(models.TextChoices):
    MONDAY    = "MONDAY", "Monday"
    TUESDAY   = "TUESDAY", "Tuesday"
    WEDNESDAY = "WEDNESDAY", "Wednesday"
    THURSDAY  = "THURSDAY", "Thursday"
    FRIDAY    = "FRIDAY", "Friday",
    SATURDAY  = 'SATURDAY', 'Saturday'
    SUNDAY    = "SUNDAY", "Sunday"

# 7. Horario de Curso
class Schedule(BaseModel):
    course = models.ForeignKey(Course, verbose_name=("Curso"), on_delete=models.CASCADE, null=True)
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
