from django.db import models
from django.db import models
from patient.models import AddedPatient
from accounts.models import CustomUser
from django.utils import timezone
# Create your models here.


class Bill(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    patient = models.ForeignKey(
        AddedPatient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    bill_date = models.DateField(
        auto_now_add=True
    )

    bill_no = models.CharField(
    max_length=30,
    unique=True,
    blank=True
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500
    )

    medicine_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    laboratory_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    room_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    other_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Pending'
    )

    def save(self,*args,**kwargs):

        if not self.bill_no:
            self.bill_no = f"BILL-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        self.total_amount = (
            self.consultation_fee +
            self.medicine_fee +
            self.laboratory_fee +
            self.room_fee +
            self.other_charges
        )

        super().save(*args,**kwargs)

    def __str__(self):
        return f"Bill-{self.id}"
    

class Payment(models.Model):

    PAYMENT_MODE = (
        ('Cash','Cash'),
        ('UPI','UPI'),
        ('Card','Card'),
        ('NetBanking','NetBanking'),
    )

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )
    receipt_no = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )
    def save(self,*args,**kwargs):

        if not self.receipt_no:
            self.receipt_no = f"REC-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        super().save(*args,**kwargs)

        self.bill.payment_status = "Paid"
        self.bill.save()

    def __str__(self):
        return self.receipt_no


class BillingHistory(models.Model):

    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=100
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.action        
