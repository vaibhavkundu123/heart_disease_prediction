from django.shortcuts import render, redirect
from .forms import RegisterForm, CodeVerificationForm
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

for user in User.objects.all():
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)


# Create your views here.
def home(request):
    return render(request, 'home.html')


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
            # Saving phone number and dob to the user profile model
            profile = UserProfile(user=user, phone_number=phone_number, dob=dob, hospital_name=hospital_name, doctor_name=doctor_name, weight=weight, blood_pressure=blood_pressure, gender=gender)
            profile.save()
            login(request, user)
            return redirect('successfully_registered')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def successfully_registered(request):
    return render(request, 'users/successfully_registered.html')


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
        
        # Ensure the user has a UserProfile
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)
        
        code = random.randint(100000, 999999)
        user.userprofile.reset_code = code
        user.userprofile.save()
        send_mail(
            'Password Reset Code',
            f'Your password reset code is {code}',
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
                # Generate URL-safe base64 encoded uid
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # Generate token
                token = default_token_generator.make_token(user)
                # Save token to user profile
                user.userprofile.reset_code = token
                user.userprofile.save()
                return redirect('password_reset_confirm', uidb64=uidb64, token=token)
            except User.DoesNotExist:
                form.add_error('code', 'Invalid code')
    else:
        form = CodeVerificationForm()
    return render(request, 'users/verify_code.html', {'form': form})


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
