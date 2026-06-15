from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from doctor.models import AddedPatient, Appointment


class DoctorSearchTests(TestCase):
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
        self.added_patient = AddedPatient.objects.create(
            doctor=self.doctor,
            name="Rohan Patil",
            mobile="9999999999",
            age=30,
            disease="Fever",
        )
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            patient_name="Rohan Patil",
            patient_mobile="9999999999",
            symptoms="Fever",
            date=timezone.now().date() + timedelta(days=1),
            time="10:30",
        )
        self.client.force_login(self.doctor)

    def test_search_patient_matches_patient_id(self):
        response = self.client.get(reverse("doctor:search_patient"), {"q": str(self.added_patient.pk)})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.added_patient.name)

    def test_search_appointment_matches_appointment_id_and_date(self):
        response = self.client.get(reverse("doctor:search_appointment"), {"q": str(self.appointment.pk)})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appointment.patient_name)

        response = self.client.get(
            reverse("doctor:search_appointment"),
            {"q": self.appointment.date.isoformat()},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.appointment.patient_name)
