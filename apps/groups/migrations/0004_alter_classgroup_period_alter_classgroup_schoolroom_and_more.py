# Generated by Django 5.1.2 on 2024-10-25 19:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_alter_classgroup_teacher'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='classgroup',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.period', verbose_name='Periodo'),
        ),
        migrations.AlterField(
            model_name='classgroup',
            name='schoolRoom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.schoolroom', verbose_name='Aula'),
        ),
        migrations.AlterField(
            model_name='classgroup',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.subject', verbose_name='Materia'),
        ),
        migrations.AlterField(
            model_name='classgroup',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Docente'),
        ),
    ]
