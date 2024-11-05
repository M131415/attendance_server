from django.conf import settings
from django.db import models

from apps.base.models import BaseModel
from apps.groups.models import ClassGroup

# Create your models here.
class Enrollments(BaseModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Estudiante",)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, verbose_name="Grupo de clases",)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

    def __str__(self):
        return f'{self.student} Grupo: {self.class_group.name}'

class Attendances(BaseModel):

    class AttendanceStatus(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        LATE = "LATE", "Late"
        ABSENT = "ABSENT", "Absent"
        LEAVE = "LEAVE", "Leave"

    enrollment = models.ForeignKey(Enrollments, on_delete=models.CASCADE, verbose_name="Inscripción",)
    attendance_status =  models.CharField(
        "Estado de asistencia", max_length=20, 
        choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT, 
    )
    observation = models.TextField('Observación', max_length=256, null=True, blank=True, )
    attendance_date = models.DateField("Fecha de asistencia", null=False, blank=False)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f'{self.enrollment} Estado: {self.attendance_status}'

