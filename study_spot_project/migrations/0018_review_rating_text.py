# Generated by Django 4.2.6 on 2023-11-07 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_spot_project', '0017_remove_review_rating_review_noise_level_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating_text',
            field=models.CharField(default='No rating', max_length=400),
            preserve_default=False,
        ),
    ]
