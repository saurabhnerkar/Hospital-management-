from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "role", "password1", "password2")

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    role = forms.ChoiceField(label="Role", choices=[
        ("admin", "Admin"),
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    ])

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label="OTP", max_length=6)
