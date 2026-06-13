from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum

from .models import Bill, Payment, BillingHistory
from .forms import BillForm, PaymentForm


# -------------------------
# Doctor Generate Bill
# -------------------------
def generate_bill(request):

    form = BillForm()

    if request.method == "POST":

        form = BillForm(request.POST)

        if form.is_valid():

            bill = form.save(commit=False)

            # Set doctor automatically
    
            bill.doctor = request.user

            bill.save()

            BillingHistory.objects.create(
                bill=bill,
                action="Bill Generated",
                description="Doctor generated bill"
            )

            return redirect('billing:bill_list')

    return render(
        request,
        'billing/generate_bill.html',
        {'form': form}
    )


# -------------------------
# Doctor Bill List
# -------------------------
def bill_list(request):

    bills = Bill.objects.all().order_by('-id')

    return render(
        request,
        'billing/bill_list.html',
        {'bills': bills}
    )


# -------------------------
# Patient Payment
# -------------------------
def make_payment(request, bill_id):

    bill = get_object_or_404(
        Bill,
        id=bill_id
    )

    form = PaymentForm()

    if request.method == "POST":

        form = PaymentForm(request.POST)

        if form.is_valid():

            payment = form.save(commit=False)

            payment.bill = bill

            payment.amount_paid = bill.total_amount

            payment.save()

            bill.payment_status = "Paid"
            bill.save()

            BillingHistory.objects.create(
                bill=bill,
                action="Payment Success",
                description=f"Payment Received ₹{bill.total_amount}"
            )

            return redirect(
                'billing:receipt',
                payment.id
            )

    return render(
        request,
        'billing/payment_form.html',
        {
            'form': form,
            'bill': bill
        }
    )


# -------------------------
# Payment History
# -------------------------
def payment_history(request):

    payments = Payment.objects.all().order_by(
        '-payment_date'
    )

    return render(
        request,
        'billing/payment_history.html',
        {
            'payments': payments
        }
    )


# -------------------------
# Receipt Page
# -------------------------
def receipt(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    return render(
        request,
        'billing/receipt.html',
        {
            'payment': payment
        }
    )


# -------------------------
# Revenue Dashboard
# -------------------------
def revenue_report(request):

    total_revenue = Payment.objects.aggregate(
        Sum('amount_paid')
    )['amount_paid__sum'] or 0

    total_payments = Payment.objects.count()

    paid_bills = Bill.objects.filter(
        payment_status='Paid'
    ).count()

    pending_bills = Bill.objects.filter(
        payment_status='Pending'
    ).count()

    return render(
        request,
        'billing/revenue_report.html',
        {
            'total_revenue': total_revenue,
            'total_payments': total_payments,
            'paid_bills': paid_bills,
            'pending_bills': pending_bills,
        }
    )


# -------------------------
# Bill Details
# -------------------------
def bill_detail(request, bill_id):

    bill = get_object_or_404(
        Bill,
        id=bill_id
    )

    history = BillingHistory.objects.filter(
        bill=bill
    ).order_by('-created_at')

    return render(
        request,
        'billing/bill_detail.html',
        {
            'bill': bill,
            'history': history
        }
    )