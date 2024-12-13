from django.conf import settings
from django.db import models

from apps.users.models import Career

from apps.base.models import BaseModel

SEMESTER_CHOICES = [
    (1, 'Primero'),
    (2, 'Segundo'),
    (3, 'Tercero'),
    (4, 'Cuarto'),
    (5, 'Quinto'),
    (6, 'Sexto'),
    (7, 'Séptimo'),
    (8, 'Octavo'),
    (9, 'Noveno'),
]

# 1. Materia 
class Subject(BaseModel):
    code       = models.CharField("Clave de la materia", max_length=64, null=False, blank=False, unique=True)
    name       = models.CharField("Nombre de la materia", max_length=255, null=False, blank=False, unique=True)
    short_name = models.CharField("Nombre Abreviado de la materia", max_length=255, null=False, blank=False, unique=True)
    semester   = models.PositiveSmallIntegerField("No. de Semestre", choices=SEMESTER_CHOICES, null=False, blank=False)
    career     = models.ForeignKey(Career, on_delete=models.CASCADE, verbose_name="Carrera", null=False, blank=False)
    image      = models.ImageField('Imagen de la materia', upload_to='materias/', max_length=255, null=True, blank=True)

    class Meta:
        ordering            = ["code", "career"]
        verbose_name        = 'Materia'
        verbose_name_plural = 'Materias'
        db_table            = 'subject'

    def __str__(self):
        return f'{self.short_name}'

# 2. Departamento
class Department(BaseModel):
    name = models.CharField("Nombre del departamento", max_length=255, null=False, blank=False, unique=True)

    class Meta:
        ordering            = ["name"]
        verbose_name        = 'Departamento'
        verbose_name_plural = 'Departamentos'
        db_table            = 'department'

    def __str__(self):
        return f'{self.name}'

# 3. Periodo
class Period(BaseModel):
    code       = models.CharField("Clave del periodo", max_length=64, null=False, blank=False, unique=True)
    name       = models.CharField('Nombre del periodo', max_length=128, null=True, blank=False, unique=True)
    start_date = models.DateField("Fecha de inicio", null=False, blank=False,)
    end_date   = models.DateField("Fecha de fin", null=False, blank=False,)

    class Meta:
        ordering            = ["start_date"]
        verbose_name        = 'Periodo'
        verbose_name_plural = 'Periodos'
        db_table            = 'period'

    def __str__(self):
        return f'{self.name}'
    
# 4. Aula
class SchoolRoom(BaseModel):
    name = models.CharField("Nombre del Aula", max_length=256, null=False, blank=False, unique=True)

    class Meta:
        ordering            = ["name"]
        verbose_name        = 'Aula'
        verbose_name_plural = 'Aulas'
        db_table            = 'school_room'

    def __str__(self):
        return f'{self.name}'

# 5. Grupo
class Group(BaseModel):
    name   = models.CharField("Nombre del grupo", max_length=256, null=False, blank=False)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Periodo", null=False, blank=False)

    class Meta:
        ordering            = ["name", "period"]
        verbose_name        = 'Grupo'
        verbose_name_plural = 'Grupos'
        db_table            = 'group'

        # Evita que un grupo se repita
        constraints = [
            models.UniqueConstraint(
                fields=["name", "period"], 
                condition=models.Q(state=True),
                name="unique_name_period",
            ),
        ]

    def __str__(self):
        return f'{self.name}'
    
    @property
    def enrollments_count(self):
        from apps.attendances.models import Enrollment
        enrollments_count = Enrollment.objects.filter(state=True ,group=self).count()
        return enrollments_count
    
    @property
    def courses_count(self):
        from apps.groups.models import Course
        courses_count = Course.objects.filter(state=True ,group=self).count()
        return courses_count

# 6. Curso
class Course(BaseModel):
    teacher     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Docente", null=True, blank=True)
    group       = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Grupo", null=False, blank=False, related_name='courses')
    subject     = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Materia", null=False, blank=False)
    school_room = models.ForeignKey(SchoolRoom, on_delete=models.CASCADE, verbose_name="Aula", null=False, blank=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Departamento", null=False, blank=False)
    period      = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name="Periodo", null=False, blank=False)

    class Meta:
        ordering            = ["teacher"]
        verbose_name        = 'Curso'
        verbose_name_plural = 'Cursos'
        db_table            = 'course'

        # Evita que un curso se repita
        constraints = [
            models.UniqueConstraint(
                fields=['teacher', 'group', 'subject', 'school_room', 'period'], 
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
    course      = models.ForeignKey(Course, verbose_name="Curso", on_delete=models.CASCADE, null=False, related_name='schedules')
    day_of_week = models.CharField( max_length=20, choices=DayOfWeek.choices, default=DayOfWeek.MONDAY)
    start_time  = models.TimeField("Hora de inicio", null=False, blank=False, )
    end_time    = models.TimeField("Hora de fin", null=False, blank=False, )

    class Meta:
        ordering            = ["start_time", "course"]
        verbose_name        = 'Horario'
        verbose_name_plural = 'Horarios'
        db_table            = 'schedule'

    def __str__(self):
        return f'{self.day_of_week} {self.start_time} : {self.end_time}'
