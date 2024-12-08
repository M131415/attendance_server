# Generated by Django 5.1.2 on 2024-10-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classgroup',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Nombre del grupo'),
        ),
        migrations.AlterField(
            model_name='departament',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Nombre del departamento'),
        ),
        migrations.AlterField(
            model_name='period',
            name='end_date',
            field=models.DateField(unique=True, verbose_name='Fecha de fin'),
        ),
        migrations.AlterField(
            model_name='period',
            name='start_date',
            field=models.DateField(unique=True, verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='schoolroom',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Nombre del Aula'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=256, unique=True, verbose_name='Nombre de la materia'),
        ),
    ]
