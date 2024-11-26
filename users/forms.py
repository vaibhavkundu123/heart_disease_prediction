from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    dob = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2024)))
    gender = forms.ChoiceField(choices=[('No Choice', 'No Choice'), ('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], required=True)
    hospital_name = forms.CharField(required=True, max_length=100)
    doctor_name = forms.CharField(required=True, max_length=100)
    weight = forms.DecimalField(required=True, max_digits=5, decimal_places=2)
    blood_pressure = forms.CharField(required=True, max_length=7)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'dob', 'gender', 'hospital_name', 'doctor_name', 'weight', 'blood_pressure', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered. Please use a different email.")
        return email


class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)


class HealthPredictionForm(forms.Form):
    height = forms.FloatField(
        label='Height (cm)', 
        min_value=0, 
        max_value=300,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    weight = forms.FloatField(
        label='Weight (kg)', 
        min_value=0, 
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    temperature = forms.FloatField(
        label='Temperature (°C)', 
        min_value=0, 
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    heart_rate = forms.FloatField(
        label='Heart Rate', 
        min_value=0, 
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    cholesterol = forms.FloatField(
        label='Cholesterol (mg/dL)', 
        min_value=0, 
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    blood_sugar = forms.FloatField(
        label='Blood Sugar (mg/dL)', 
        min_value=0, 
        max_value=500,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    systolic = forms.FloatField(
        label='Systolic Pressure', 
        min_value=0, 
        max_value=250,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    diastolic = forms.FloatField(
        label='Diastolic Pressure', 
        min_value=0, 
        max_value=200,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    symptoms = forms.ChoiceField(
        choices=[
            ('Chest Pain', 'Chest Pain'),
            ('Shortness of Breath', 'Shortness of Breath'),
            ('Fainting', 'Fainting'),
            ('Nausea', 'Nausea'),
            ('Vomiting', 'Vomiting'),
            ('Diarrhea', 'Diarrhea'),
            ('Unknown', 'Unknown')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    existing_conditions = forms.ChoiceField(
        choices=[
            ('Diabetes', 'Diabetes'),
            ('Hypertension', 'Hypertension'),
            ('High Cholesterol', 'High Cholesterol'),
            ('Asthma', 'Asthma'),
            ('Unknown', 'Unknown')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    laboratory_test_results = forms.ChoiceField(
        choices=[
            ('High Cholesterol', 'High Cholesterol'),
            ('High Blood Sugar', 'High Blood Sugar'),
            ('Normal', 'Normal'),
            ('Low Iron', 'Low Iron'),
            ('Unknown', 'Unknown')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    family_history = forms.ChoiceField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
            ('Unknown', 'Unknown')
        ],
        label='Family History of Heart Disease',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    smoking_status = forms.ChoiceField(
        choices=[
            ('Never', 'Never'),
            ('Former', 'Former'),
            ('Current', 'Current'),
            ('Unknown', 'Unknown')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )