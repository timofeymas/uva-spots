# Generated by Django 4.2.6 on 2023-12-02 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study_spot_project', '0023_unacceptedplace_rejection_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='unacceptedplace',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
