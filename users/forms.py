from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    dob = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2024)))
    hospital_name = forms.CharField(required=True, max_length=100)
    doctor_name = forms.CharField(required=True, max_length=100)
    weight = forms.DecimalField(required=True, max_digits=5, decimal_places=2)
    blood_pressure = forms.CharField(required=True, max_length=7)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'dob', 'hospital_name', 'doctor_name', 'weight', 'blood_pressure', 'password1', 'password2']
