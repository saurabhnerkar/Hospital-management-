from django.contrib import admin
from .models import CustomUser, Specialization, LoginOTP

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_email_verified')
    list_filter = ('role', 'is_email_verified')
    search_fields = ('email', 'username')

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_used', 'expires_at', 'created_at')
    list_filter = ('is_used', 'created_at')