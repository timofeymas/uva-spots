# Generated by Django 4.2.6 on 2023-12-02 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_spot_project', '0022_rename_has_seen_welcome_modal_userprofile_has_seen_modal'),
    ]

    operations = [
        migrations.AddField(
            model_name='unacceptedplace',
            name='rejection_message',
            field=models.CharField(default='', max_length=200),
        ),
    ]
