from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from doctor.models import Appointment


class AdminPanelTests(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="password123",
            role="admin",
        )
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
            patient_mobile="7777777777",
            symptoms="Consultation",
            date=timezone.now().date() + timedelta(days=1),
            time="09:00",
        )
        self.client.force_login(self.admin)

    def test_admin_can_approve_appointment(self):
        response = self.client.post(
            reverse("adminpanel:approve_appointment", args=[self.appointment.pk]),
            follow=True,
        )

        self.appointment.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.appointment.status, "Approved")

    def test_registered_users_lists_all_non_current_users(self):
        response = self.client.get(reverse("adminpanel:registered_users"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor.email)
        self.assertContains(response, self.patient.email)
        self.assertNotContains(response, self.admin.email)
