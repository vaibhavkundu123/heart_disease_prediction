from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('No Choice', 'No Choice'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    hospital_name = models.CharField(blank=True, max_length=100)
    doctor_name = models.CharField(blank=True, max_length=100)
    weight = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    blood_pressure = models.CharField(blank=True, max_length=7)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, default='No Choice')
    reset_code = models.CharField(max_length=6, blank=True, null=True)