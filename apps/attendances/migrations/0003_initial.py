# Generated by Django 5.1.3 on 2024-12-03 04:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attendances', '0002_initial'),
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Estudiante'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendances.enrollment', verbose_name='Inscripción'),
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='course',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='groups.course', verbose_name='Curso'),
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='enrollment',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='attendances.enrollment', verbose_name='Inscripción'),
        ),
        migrations.AddField(
            model_name='historicalattendance',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalenrollment',
            name='group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='groups.group', verbose_name='Grupo'),
        ),
        migrations.AddField(
            model_name='historicalenrollment',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalenrollment',
            name='student',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante'),
        ),
        migrations.AddConstraint(
            model_name='enrollment',
            constraint=models.UniqueConstraint(condition=models.Q(('state', True)), fields=('student', 'group'), name='unique_inscripcion'),
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(condition=models.Q(('state', True)), fields=('enrollment', 'course', 'attendance_date'), name='unique_attendance'),
        ),
    ]
