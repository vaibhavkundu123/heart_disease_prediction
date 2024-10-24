from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def send_registration_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to My Website'
        message = f'Hi {instance.username}, thank you for registering at My Website.'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, email_from, recipient_list)