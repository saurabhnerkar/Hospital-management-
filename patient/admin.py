from django.contrib import admin
from .models import PatientProfile, AddedPatient

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth')
    search_fields = ('user__email', 'phone_number')

@admin.register(AddedPatient)
class AddedPatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'doctor', 'disease', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'mobile')
