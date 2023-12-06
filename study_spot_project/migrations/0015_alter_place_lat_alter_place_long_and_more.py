# Generated by Django 4.2.6 on 2023-11-04 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_spot_project', '0014_alter_unacceptedplace_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.DecimalField(decimal_places=16, max_digits=20),
        ),
        migrations.AlterField(
            model_name='place',
            name='long',
            field=models.DecimalField(decimal_places=16, max_digits=20),
        ),
        migrations.AlterField(
            model_name='unacceptedplace',
            name='lat',
            field=models.DecimalField(decimal_places=16, max_digits=20),
        ),
        migrations.AlterField(
            model_name='unacceptedplace',
            name='long',
            field=models.DecimalField(decimal_places=16, max_digits=20),
        ),
    ]
