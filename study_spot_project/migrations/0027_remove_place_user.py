# Generated by Django 4.2.6 on 2023-12-03 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study_spot_project', '0026_place_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='user',
        ),
    ]
