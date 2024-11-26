from django.shortcuts import render, redirect
from .forms import RegisterForm, CodeVerificationForm, HealthPredictionForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
import random
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils import timezone
from datetime import timedelta
from .models import PredictionResult
import os
from django.contrib.auth import logout
from .predictor import HealthPredictor


# for user in User.objects.all():
#     if not hasattr(user, 'userprofile'):
#         UserProfile.objects.create(user=user)


# Create your views here.
def home(request):
    return render(request, 'users/home.html')


def successfully_registered(request):
    return render(request, 'users/successfully_registered.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            dob = form.cleaned_data.get('dob')
            hospital_name = form.cleaned_data.get('hospital_name')
            doctor_name = form.cleaned_data.get('doctor_name')
            weight = form.cleaned_data.get('weight')
            blood_pressure = form.cleaned_data.get('blood_pressure')
            gender = form.cleaned_data.get('gender')
            # Check if the user already has a profile
            if not hasattr(user, 'userprofile'):
                profile = UserProfile(
                    user=user, 
                    phone_number=phone_number, 
                    dob=dob, 
                    hospital_name=hospital_name, 
                    doctor_name=doctor_name, 
                    weight=weight, 
                    blood_pressure=blood_pressure, 
                    gender=gender
                )
                profile.save()
            login(request, user)
            return redirect('successfully_registered')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        self.send_login_confirmation_email(user)
        return redirect(self.get_success_url())


def send_login_confirmation_email(user):
    subject = 'Login Successful'
    message = f'Hi {user.username}, you have successfully logged in to My Website.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)


def login_view(request):  # don't name "login" bcoz django already have build-in log in function"
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                send_login_confirmation_email(user)
                return redirect('successfully_logged_in')  # Redirect successful login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required  # Ensure the user is logged in before accessing this view
def successfully_logged_in(request):
    return render(request, 'users/successfully_logged_in.html')


# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'users/password_reset.html'
#     email_template_name = 'users/password_reset_email.html'
#     success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)
        
        code = random.randint(100000, 999999)
        user.userprofile.reset_code = code
        user.userprofile.reset_code_timestamp = timezone.now()
        user.userprofile.save()
        send_mail(
            'Password Reset Code',
            f'Your password reset code is {code}. This code will expire in 5 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        return redirect('verify_code')
    

def verify_code(request):
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(userprofile__reset_code=code)
                time_limit = timezone.now() - timedelta(minutes=5)
                if user.userprofile.reset_code_timestamp < time_limit:
                    return render(request, 'users/verify_code.html', {
                        'expired': True
                    })
                # ... rest of the validation logic
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                user.userprofile.reset_code = token
                user.userprofile.save()
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)
            except User.DoesNotExist:
                form.add_error('code', 'Invalid code')
    else:
        form = CodeVerificationForm()
    
    context = {
        'form': form,
        'start_time': request.session.get('reset_code_timestamp', timezone.now().isoformat()),
        'expired': False
    }
    return render(request, 'users/verify_code.html', context)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'users/password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = SetPasswordForm
    token_generator = default_token_generator
    
    def dispatch(self, *args, **kwargs):
        if 'uidb64' in kwargs and 'token' in kwargs:
            self.kwargs['uidb64'] = kwargs['uidb64'] 
            self.kwargs['token'] = kwargs['token']
        return super().dispatch(*args, **kwargs)

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


@login_required
def prediction_view(request):
    if request.method == 'POST':
        form = HealthPredictionForm(request.POST)
        if form.is_valid():
            # Get cleaned data from form
            patient_data = {
                'Height_cm': form.cleaned_data['height'],
                'Weight_kg': form.cleaned_data['weight'],
                'Temperature_C': form.cleaned_data['temperature'],
                'Heart_Rate': form.cleaned_data['heart_rate'],
                'Cholesterol_mg_dL': form.cleaned_data['cholesterol'],
                'Blood_Sugar_mg_dL': form.cleaned_data['blood_sugar'],
                'Systolic': form.cleaned_data['systolic'],
                'Diastolic': form.cleaned_data['diastolic'],
                'Symptoms': form.cleaned_data['symptoms'],
                'Existing_Conditions': form.cleaned_data['existing_conditions'],
                'Laboratory_Test_Results': form.cleaned_data['laboratory_test_results'],
                'Family_History_Heart_Disease': form.cleaned_data['family_history'],
                'Smoking_Status': form.cleaned_data['smoking_status']
            }

            # Initialize predictor and make prediction
            predictor = HealthPredictor()
            result = predictor.predict(patient_data)

            if result and 'error' not in result:
                # Check if the result has the expected keys
                if 'predicted_disease' in result and 'confidence_score' in result:
                    # Save prediction to database
                    prediction = PredictionResult(
                        user=request.user,
                        height=patient_data['Height_cm'],
                        weight=patient_data['Weight_kg'],
                        temperature=patient_data['Temperature_C'],
                        heart_rate=patient_data['Heart_Rate'],
                        cholesterol=patient_data['Cholesterol_mg_dL'],
                        blood_sugar=patient_data['Blood_Sugar_mg_dL'],
                        systolic=patient_data['Systolic'],
                        diastolic=patient_data['Diastolic'],
                        symptoms=patient_data['Symptoms'],
                        existing_conditions=patient_data['Existing_Conditions'],
                        laboratory_test_results=patient_data['Laboratory_Test_Results'],
                        family_history=patient_data['Family_History_Heart_Disease'],
                        smoking_status=patient_data['Smoking_Status'],
                        predicted_disease=result['predicted_disease'],
                        confidence_score=result['confidence_score']
                    )
                    prediction.save()

                    return render(request, 'users/result.html', {
                        'result': result,
                        'patient_data': patient_data
                    })
                else:
                    # Handle case where result doesn't have expected keys
                    return render(request, 'predictor/error.html', {
                        'error_message': 'Prediction result is incomplete or invalid.'
                    })
            else:
                # Handle prediction failure or error
                return render(request, 'predictor/error.html', {
                    'error_message': 'Prediction failed. Please try again later.'
                })
    else:
        form = HealthPredictionForm()

    return render(request, 'users/predictionform.html', {'form': form})


# def login_view(request):  #dont name "login" bcoz django already have build-in log in function"
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('dashboard_view')  # Redirect prediction view
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@login_required
def view_history(request):
    # Get the user's prediction history (assuming predictions are stored with a user reference)
    history = PredictionResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/view_history.html', {'history': history})


def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('login')  # Redirects the user to the login page