from django.db.models.signals import post_save
from django.dispatch import receiver

def create_profile(sender, instance, created, **kwargs):
    if created:
        from .models import Profile
        Profile.objects.create(user=instance)

def ready():
    from django.contrib.auth.models import User
    post_save.connect(create_profile, sender=User)