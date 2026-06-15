from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from billing.forms import BillForm
from billing.models import Bill, Payment
from doctor.models import AddedPatient


class BillingTests(TestCase):
    def setUp(self):
        self.doctor_one = CustomUser.objects.create_user(
            email="doctor1@example.com",
            password="password123",
            role="doctor",
            fees=Decimal("750.00"),
        )
        self.doctor_two = CustomUser.objects.create_user(
            email="doctor2@example.com",
            password="password123",
            role="doctor",
        )
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="password123",
            role="admin",
        )
        self.patient_user = CustomUser.objects.create_user(
            email="patient@example.com",
            password="password123",
            role="patient",
        )
        self.patient_one = AddedPatient.objects.create(
            doctor=self.doctor_one,
            name="Patient One",
            mobile="9991112222",
            age=28,
            disease="Flu",
        )
        self.patient_two = AddedPatient.objects.create(
            doctor=self.doctor_two,
            name="Patient Two",
            mobile="9993334444",
            age=34,
            disease="Cold",
        )

    def test_bill_form_limits_patients_to_current_doctor(self):
        form = BillForm(user=self.doctor_one)

        self.assertEqual(list(form.fields["patient"].queryset), [self.patient_one])

    def test_bill_form_uses_doctor_fees_as_default_consultation_fee(self):
        form = BillForm(user=self.doctor_one)

        self.assertEqual(form.fields["consultation_fee"].initial, Decimal("750.00"))

    def test_bill_list_shows_only_current_doctors_bills(self):
        own_bill = Bill.objects.create(
            patient=self.patient_one,
            doctor=self.doctor_one,
            consultation_fee=Decimal("500.00"),
            medicine_fee=Decimal("100.00"),
            laboratory_fee=Decimal("50.00"),
            room_fee=Decimal("0.00"),
            other_charges=Decimal("25.00"),
        )
        other_bill = Bill.objects.create(
            patient=self.patient_two,
            doctor=self.doctor_two,
            consultation_fee=Decimal("600.00"),
            medicine_fee=Decimal("50.00"),
            laboratory_fee=Decimal("25.00"),
            room_fee=Decimal("0.00"),
            other_charges=Decimal("10.00"),
        )

        self.client.force_login(self.doctor_one)
        response = self.client.get(reverse("billing:bill_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, own_bill.bill_no)
        self.assertNotContains(response, other_bill.bill_no)

    def test_doctor_can_record_payment_for_own_bill(self):
        bill = Bill.objects.create(
            patient=self.patient_one,
            doctor=self.doctor_one,
            consultation_fee=Decimal("500.00"),
        )

        self.client.force_login(self.doctor_one)
        response = self.client.post(
            reverse("billing:payment", args=[bill.id]),
            {"payment_mode": "Cash"},
        )

        self.assertEqual(response.status_code, 302)
        bill.refresh_from_db()
        self.assertEqual(bill.payment_status, "Paid")
        self.assertEqual(Payment.objects.filter(bill=bill).count(), 1)

    def test_doctor_cannot_record_payment_for_other_doctors_bill(self):
        bill = Bill.objects.create(
            patient=self.patient_two,
            doctor=self.doctor_two,
            consultation_fee=Decimal("500.00"),
        )

        self.client.force_login(self.doctor_one)
        response = self.client.post(
            reverse("billing:payment", args=[bill.id]),
            {"payment_mode": "Cash"},
        )

        self.assertEqual(response.status_code, 404)
        bill.refresh_from_db()
        self.assertEqual(bill.payment_status, "Pending")

    def test_paid_bill_cannot_be_paid_again(self):
        bill = Bill.objects.create(
            patient=self.patient_one,
            doctor=self.doctor_one,
            consultation_fee=Decimal("500.00"),
            payment_status="Paid",
        )
        Payment.objects.create(
            bill=bill,
            amount_paid=bill.total_amount,
            payment_mode="Cash",
        )

        self.client.force_login(self.doctor_one)
        response = self.client.get(reverse("billing:payment", args=[bill.id]))

        self.assertRedirects(response, reverse("billing:bill_detail", args=[bill.id]))

    def test_patient_cannot_access_billing_pages(self):
        self.client.force_login(self.patient_user)

        for url_name in (
            "billing:generate_bill",
            "billing:bill_list",
            "billing:payment_history",
            "billing:revenue_report",
        ):
            response = self.client.get(reverse(url_name))
            self.assertNotEqual(response.status_code, 200)

    def test_admin_doctor_revenue_report_shows_per_doctor_totals(self):
        bill_one = Bill.objects.create(
            patient=self.patient_one,
            doctor=self.doctor_one,
            consultation_fee=Decimal("500.00"),
            payment_status="Paid",
        )
        bill_two = Bill.objects.create(
            patient=self.patient_two,
            doctor=self.doctor_two,
            consultation_fee=Decimal("300.00"),
            payment_status="Paid",
        )
        Payment.objects.create(bill=bill_one, amount_paid=bill_one.total_amount, payment_mode="Cash")
        Payment.objects.create(bill=bill_two, amount_paid=bill_two.total_amount, payment_mode="UPI")

        self.client.force_login(self.admin)
        response = self.client.get(reverse("adminpanel:doctor_revenue_report"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "doctor1@example.com")
        self.assertContains(response, "doctor2@example.com")
        self.assertContains(response, "Rs. 500")
        self.assertContains(response, "Rs. 300")

    def test_doctor_revenue_report_shows_only_own_totals(self):
        own_bill = Bill.objects.create(
            patient=self.patient_one,
            doctor=self.doctor_one,
            consultation_fee=Decimal("500.00"),
            payment_status="Paid",
        )
        other_bill = Bill.objects.create(
            patient=self.patient_two,
            doctor=self.doctor_two,
            consultation_fee=Decimal("900.00"),
            payment_status="Paid",
        )
        Payment.objects.create(bill=own_bill, amount_paid=own_bill.total_amount, payment_mode="Cash")
        Payment.objects.create(bill=other_bill, amount_paid=other_bill.total_amount, payment_mode="Cash")

        self.client.force_login(self.doctor_one)
        response = self.client.get(reverse("billing:revenue_report"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rs. 500")
        self.assertNotContains(response, "Rs. 900")
