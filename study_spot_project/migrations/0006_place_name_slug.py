# Generated by Django 4.2.6 on 2023-10-19 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_spot_project', '0005_place_place_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='name_slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', unique=True),
        ),
    ]