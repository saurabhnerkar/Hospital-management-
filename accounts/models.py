import uuid
import random
from datetime import timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


# ======================================================
# CUSTOM USER MANAGER
# ======================================================
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, role="patient", **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)

        # auto-fill username (AbstractUser requirement)
        user.username = email.split("@")[0]

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, role="admin", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if role != "admin":
            role = "admin"

        return self.create_user(email, password, role=role, **extra_fields)



# ======================================================
# CUSTOM USER MODEL
# ======================================================
class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    )

    # username = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")



    # ---------------------------
    # DOCTOR EXTRA FIELDS (NEW)
    # ---------------------------
    education = models.CharField(max_length=200, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    fees = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    specialization = models.ForeignKey(
        "Specialization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # ---------------------------

    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)

    # OTP helpers
    def generate_email_verification_token(self):
        self.email_verification_token = uuid.uuid4()
        self.save(update_fields=["email_verification_token"])
        return self.email_verification_token

    def generate_login_otp(self):
        LoginOTP.objects.filter(user=self, is_used=False).update(is_used=True)

        otp = "".join([str(random.randint(0, 9)) for _ in range(6)])

        LoginOTP.objects.create(
            user=self,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        return otp



# ======================================================
# SPECIALIZATION MODEL
# ======================================================
class Specialization(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title



# ======================================================
# OTP MODEL
# ======================================================
class LoginOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"OTP for {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        return not self.is_expired() and not self.is_used
