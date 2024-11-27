from django.conf import settings
from django.db import models

from apps.base.models import BaseModel
from apps.groups.models import Group, Course
# Create your models here.
class Enrollments(BaseModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Estudiante",)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Grupo", null=True)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

        # Evita que un estudiante se inscriba más de una vez al mismo grupo
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'group'], 
                condition=models.Q(state=True),
                name='unique_inscripcion', 
            ),
        ]

    def __str__(self):
        return f'{self.student} Grupo: {self.group}'

class Attendances(BaseModel):

    class AttendanceStatus(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        LATE = "LATE", "Late"
        ABSENT = "ABSENT", "Absent"
        LEAVE = "LEAVE", "Leave"

    enrollment = models.ForeignKey(Enrollments, on_delete=models.CASCADE, verbose_name="Inscripción",)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso", null=True)
    attendance_status =  models.CharField(
        "Estado de asistencia", max_length=20, 
        choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT, 
    )
    observation = models.TextField('Observación', max_length=256, null=True, blank=True, )
    attendance_date = models.DateField("Fecha de asistencia", null=False, blank=False)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

        # Evita que una inscripcion tenga mas de una asistencia por dia
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'course','attendance_date'], 
                condition=models.Q(state=True),
                name='unique_attendance'
            )
        ]

    def __str__(self):
        return f'{self.enrollment} Estado: {self.attendance_status}'

