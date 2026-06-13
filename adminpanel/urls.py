from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="dashboard"),
    path("doctors/", views.doctors_list, name="doctors_list"),
    path("doctor/<int:pk>/profile/", views.doctor_profile, name="doctor_profile"),
    path("doctor/<int:pk>/appointments/", views.doctor_appointments, name="doctor_appointments"),
    path("doctor/<int:pk>/patients/", views.doctor_patients, name="doctor_patients"),
    path("users/", views.registered_users, name="registered_users"),
    path("users/<int:pk>/delete/", views.delete_user, name="delete_user"),
    path("patients/", views.patients_list, name="patients_list"),
    path("patients/<int:pk>/delete/", views.delete_patient, name="delete_patient"),
    path("appointments/", views.appointment_history, name="appointments"),
    path("search/doctor/", views.search_doctor, name="search_doctor"),
    path("search/patient/", views.search_patient, name="search_patient"),
    path("reports/doctor/", views.doctor_report, name="doctor_report"),
    path("webpage/", views.webpage_update, name="webpage_update"),
    path("profile/", views.admin_profile, name="admin_profile"),
    path("change-password/", views.admin_change_password, name="admin_change_password"),
]
