from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


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
    reset_code_timestamp = models.DateTimeField(null=True, blank=True)


class PredictionResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    height = models.FloatField()
    weight = models.FloatField()
    temperature = models.FloatField()
    heart_rate = models.IntegerField()
    cholesterol = models.IntegerField()
    blood_sugar = models.IntegerField()
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    symptoms = models.CharField(max_length=255, default='Unknown')
    existing_conditions = models.CharField(max_length=255, default='Unknown')
    laboratory_test_results = models.CharField(max_length=255, default='Unknown')
    family_history = models.CharField(max_length=255, default='Unknown')
    smoking_status = models.CharField(max_length=255, default='Unknown')
    predicted_disease = models.CharField(max_length=255, default='Unknown')
    confidence_score = models.FloatField()

    # Automatically set the current timestamp when the record is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.predicted_disease} with {self.confidence_score}% confidence"