from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import UserProfile


@receiver(post_save, sender=User)
def send_registration_confirmation(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to My Website'
        message = f'Hi {instance.username}, thank you for registering at My Website.'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, email_from, recipient_list)


# @receiver(user_logged_in)
# def send_login_confirmation(sender, request, user, **kwargs):
#     subject = 'Login Successful'
#     message = f'Hi {user.username}, you have successfully logged in to My Website.'
#     email_from = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user.email]
#     send_mail(subject, message, email_from, recipient_list)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()