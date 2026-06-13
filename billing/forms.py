from django import forms
from .models import Bill
from .models import Payment


class BillForm(forms.ModelForm):

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

