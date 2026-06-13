from django.db import models
from accounts.models import CustomUser



class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="doctor_appointments")
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="patient_appointments", null=True, blank=True)
    symptoms = models.TextField(blank=True, null=True)

    # If patient not registered (optional)
    patient_name = models.CharField(max_length=100)
    patient_mobile = models.CharField(max_length=15)

    date = models.DateField()
    time = models.TimeField()

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} -> {self.doctor.email} ({self.date})"



class AddedPatient(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    age = models.IntegerField()
    disease = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Dr. {self.doctor.email})"
