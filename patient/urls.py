from django.urls import path
from . import views

app_name = "patient"

urlpatterns = [
    path("dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("appointments/", views.appointment_history, name="appointment_history"),
    path("appointments/<int:pk>/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("profile/", views.patient_profile, name="patient_profile"),
    path("change-password/", views.patient_change_password, name="patient_change_password"),
    path("appointment-report/", views.appointment_report, name="appointment_report"),
]
