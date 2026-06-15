from pathlib import Path

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from .forms import CustomUserCreationForm, OTPVerificationForm, LoginForm
from .models import CustomUser, LoginOTP


HOMEPAGE_CONTENT_PATH = Path(settings.BASE_DIR) / "homepage_content.txt"
DEFAULT_HOMEPAGE_CONTENT = (
    "Bring clinicians, patients, and operational teams into one connected care "
    "workspace with faster scheduling, clearer decisions, and a calmer day-to-day experience."
)


def load_homepage_content():
    try:
        content = HOMEPAGE_CONTENT_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        content = ""

    return content or DEFAULT_HOMEPAGE_CONTENT


def home(request):
    return render(request, "home.html", {"homepage_content": load_homepage_content()})
    

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            otp = user.generate_login_otp()

            send_mail(
                "Your Verification OTP",
                f"Your OTP is: {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            request.session['otp_email'] = user.email
            messages.success(request, "Registration successful! OTP sent to your email.")
            return redirect("accounts:verify_otp")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def verify_otp(request):
    # Check if there's a pending OTP in session
    if 'otp_email' not in request.session:
        messages.error(request, "No pending verification found. Please register first.")
        return redirect("accounts:register")
    
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            email = request.session.get("otp_email")

            try:
                user = CustomUser.objects.get(email=email)
                otp_record = LoginOTP.objects.filter(
                    user=user, otp=otp, is_used=False, expires_at__gt=timezone.now()
                ).first()

                if otp_record:
                    otp_record.is_used = True
                    otp_record.save()

                    user.is_active = True
                    user.is_email_verified = True
                    user.save()

                    # Clear session
                    del request.session["otp_email"]
                    
                    messages.success(request, "Email verified successfully! Please log in.")
                    return redirect("accounts:login")
                else:
                    messages.error(request, "Invalid or expired OTP. Please try again.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found. Please register again.")
                return redirect("accounts:register")
    else:
        form = OTPVerificationForm()

    return render(request, "accounts/verify_otp.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            role = form.cleaned_data["role"]

            user = authenticate(request, email=email, password=password)

            if user is None:
                messages.error(request, "Invalid email or password.")
                return render(request, "accounts/login.html", {"form": form})

           
            if user.role != "admin" and not user.is_active:
                messages.error(request, "Account inactive. Verify your email first.")
                return render(request, "accounts/login.html", {"form": form})

            if user.role != role:
                messages.error(request, "Incorrect role selected!")
                return render(request, "accounts/login.html", {"form": form})

      
            login(request, user)

            if user.role == "admin":
                return redirect("adminpanel:dashboard")
            elif user.role == "doctor":
                return redirect("doctor:doctor_dashboard")
            else:
                return redirect("patient:patient_dashboard")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("accounts:home")
