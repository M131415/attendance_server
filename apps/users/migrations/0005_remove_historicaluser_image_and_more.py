# Generated by Django 5.1.2 on 2024-10-25 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_studentprofile_teacherprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='image',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='historicaluser',
            name='is_teacher',
        ),
        migrations.RemoveField(
            model_name='user',
            name='image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_teacher',
        ),
        migrations.AddField(
            model_name='historicaluser',
            name='rol',
            field=models.CharField(choices=[('TEACHER', 'Teacher'), ('STUDENT', 'Student')], default='STUDENT', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.CharField(choices=[('TEACHER', 'Teacher'), ('STUDENT', 'Student')], default='STUDENT', max_length=20),
        ),
    ]
