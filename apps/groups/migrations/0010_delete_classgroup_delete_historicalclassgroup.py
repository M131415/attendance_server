# Generated by Django 5.1.3 on 2024-11-21 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0007_attendances_course_historicalattendances_course_and_more'),
        ('groups', '0009_remove_classgroup_period_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClassGroup',
        ),
        migrations.DeleteModel(
            name='HistoricalClassGroup',
        ),
    ]
