from django.contrib import admin
from .models import Appointment, AddedPatient

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('patient_name', 'patient_mobile')

@admin.register(AddedPatient)
class DoctorAddedPatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'doctor', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'mobile')
