from django import forms
from .models import Bill
from .models import Payment


class BillForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        patients = self.fields["patient"].queryset.select_related("doctor").order_by("name")
        if user is not None:
            patients = patients.filter(doctor=user)
            if user.fees and not self.instance.pk:
                self.fields["consultation_fee"].initial = user.fees
        self.fields["patient"].queryset = patients

    class Meta:
        model = Bill

        fields = [
            'patient',
            'consultation_fee',
            'medicine_fee',
            'laboratory_fee',
            'room_fee',
            'other_charges'
        ]

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            'payment_mode',
            'transaction_id',
            'remarks'
        ]

