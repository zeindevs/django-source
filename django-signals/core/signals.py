import os

from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.models import User


@receiver(post_delete, sender=User)
def delete_associated_file(sender, instance, **kwargs):
    """Delete the file form the filesytem if it exists"""
    if instance.cv:
        if os.path.isfile(instance.cv.path):
            os.remove(instance.cv.path)


@receiver(post_save, sender=User, dispatch_uid="send_welcome_email")
def send_welcome_email(sender, instance, created, **kwargs):
    """Send a welcome email when a new user is created."""
    print("Signal fired...")
    if created:
        send_mail(
            "Welcome!",
            "Thanks for signing up!",
            "admin@django.com",
            [instance.email],
            fail_silently=False,
        )
