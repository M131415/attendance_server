# Generated by Django 5.1.3 on 2024-11-23 06:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_delete_classgroup_delete_historicalclassgroup'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='course',
            constraint=models.UniqueConstraint(fields=('teacher', 'group', 'subject', 'period'), name='unique_course'),
        ),
    ]
