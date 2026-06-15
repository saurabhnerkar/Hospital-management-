from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from doctor.models import Appointment


class PatientAppointmentTests(TestCase):
    def setUp(self):
        self.doctor = CustomUser.objects.create_user(
            email="doctor@example.com",
            password="password123",
            role="doctor",
        )
        self.patient = CustomUser.objects.create_user(
            email="patient@example.com",
            password="password123",
            role="patient",
        )
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            patient_name="Patient User",
            patient_mobile="8888888888",
            symptoms="Checkup",
            date=timezone.now().date() + timedelta(days=2),
            time="11:00",
            status="Approved",
        )

    def test_patient_can_cancel_upcoming_appointment(self):
        self.client.force_login(self.patient)

        response = self.client.post(
            reverse("patient:cancel_appointment", args=[self.appointment.pk]),
            follow=True,
        )

        self.appointment.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.appointment.status, "Cancelled")
