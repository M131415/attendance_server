from django.conf import settings
from django.db import models
from apps.groups.models import ClassGroup
# Create your models here.
class Enrollments(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classGroup = models.OneToOneField(ClassGroup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

    def __str__(self):
        return f'{self.student} {self.classGroup}'

class Attendances(models.Model):

    class AttendanceStatus(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        LATE = "LATE", "Late"
        ABSENT = "ABSENT", "Absent"
        LEAVE = "LEAVE", "Leave"

    enrollment = models.ForeignKey(Enrollments, on_delete=models.CASCADE)
    attendance_status =  models.CharField(
        max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT
    )
    observation = models.TextField('Observación', max_length=256, null=True, blank=True)
    attendance_date = models.DateField("Fecha de asistencia", null=False, blank=False, unique=True)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f'{self.enrollment} Estado: {self.attendance_status}'