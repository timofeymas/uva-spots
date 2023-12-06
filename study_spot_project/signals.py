from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile


# REFERENCES
# Title: CookieCutter adding Users to a Group with Permissions
# Date: 9/2020
# URL: https://forum.djangoproject.com/t/cookiecutter-adding-users-to-a-group-with-permissions/4297

@receiver(post_save, sender=User)
def add_user_to_users_group(sender, instance, created, **kwargs):
    if created and not instance.groups.filter(name='Admin').exists():
        UserProfile.objects.get_or_create(user=instance, defaults={'has_seen_modal': False})

        