from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Specialization, LoginOTP

admin.site.register(CustomUser)
admin.site.register(Specialization)
admin.site.register(LoginOTP)