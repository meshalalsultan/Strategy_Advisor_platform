# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender='users.CustomUser')
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.__class__.__name__ == "CustomUser":
        Profile = apps.get_model('users', 'Profile')
        Profile.objects.create(user=instance)

@receiver(post_save, sender='users.CustomUser')
def save_user_profile(sender, instance, **kwargs):
    if instance.__class__.__name__ == "CustomUser":
        instance.profile.save()