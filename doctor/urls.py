from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    path("dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("appointments/", views.doctor_appointments, name="doctor_appointments"),
    path("appointments/<int:pk>/approve/", views.approve_appointment, name="approve_appointment"),
    path("appointments/<int:pk>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("patients/", views.doctor_patients, name="doctor_patients"),
    path("patients/add/", views.add_patient, name="add_patient"),
    path("patients/<int:pk>/edit/", views.edit_patient, name="edit_patient"),
    path("search/patient/", views.search_patient, name="search_patient"),
    path("search/appointment/", views.search_appointment, name="search_appointment"),
    path("report/appointments/", views.report_appointments, name="report_appointments"),
    path("report/patients/", views.report_patients, name="report_patients"),
    path("export/appointments/excel/", views.export_appointments_excel, name="export_appointments_excel"),
    path("export/appointments/pdf/", views.export_appointments_pdf, name="export_appointments_pdf"),
    path("export/patients/excel/", views.export_patients_excel, name="export_patients_excel"),
    path("export/patients/pdf/", views.export_patients_pdf, name="export_patients_pdf"),
    path("profile/", views.doctor_profile, name="doctor_profile"),
    path("profile/change-password/", views.doctor_change_password, name="doctor_change_password"),
]
