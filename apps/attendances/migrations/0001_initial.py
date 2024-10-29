# Generated by Django 5.1.2 on 2024-10-25 16:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0002_alter_classgroup_name_alter_departament_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classGroup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='groups.classgroup')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_status', models.CharField(choices=[('PRESENT', 'Present'), ('LATE', 'Late'), ('ABSENT', 'Absent'), ('LEAVE', 'Leave')], default='PRESENT', max_length=20)),
                ('observation', models.TextField(max_length=256, verbose_name='Observación')),
                ('attendance_date', models.DateField(auto_now_add=True, unique=True, verbose_name='Fecha de asistencia')),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendances.enrollments')),
            ],
        ),
    ]
