from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BillForm, PaymentForm
from .models import Bill, BillingHistory, Payment


def is_doctor(user):
    return user.is_authenticated and user.role == "doctor"


# -------------------------
# Doctor Generate Bill
# ----------@login_required

@user_passes_test(is_doctor)
def generate_bill(request):

    patient_id = request.GET.get("patient_id")

    if request.method == "POST":

        form = BillForm(request.POST, user=request.user)

        if form.is_valid():

            bill = form.save(commit=False)
            if patient_id:
                from doctor.models import AddedPatient

                patient = get_object_or_404(
                    AddedPatient,
                    id=patient_id,
                    doctor=request.user
                )

                bill.patient = patient

            bill.doctor = request.user
            bill.save()

            BillingHistory.objects.create(
                bill=bill,
                action="Bill Generated",
                description="Doctor generated bill",
            )

            messages.success(request, "Bill generated successfully.")

            
            return redirect("billing:payment", bill.id)

    else:

        form = BillForm(user=request.user)

        if patient_id:
            form.fields['patient'].initial = patient_id

    return render(
        request,
        "billing/generate_bill.html",
        {"form": form}
    )


# -------------------------
# Doctor Bill List
# -------------------------
@login_required
@user_passes_test(is_doctor)
def bill_list(request):
    bills = (
        Bill.objects.select_related("patient", "doctor")
        .filter(doctor=request.user)
        .order_by("-id")
    )
    return render(request, "billing/bill_list.html", {"bills": bills})


# -------------------------
# Doctor Record Payment
# -------------------------
@login_required
@user_passes_test(is_doctor)
def make_payment(request, bill_id):
    bill = get_object_or_404(
        Bill.objects.select_related("patient", "doctor"),
        id=bill_id,
        doctor=request.user,
    )

    if bill.payment_status == "Paid":
        messages.info(request, "This bill has already been paid.")
        return redirect("billing:bill_detail", bill.id)

    form = PaymentForm()

    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.amount_paid = bill.total_amount
            payment.save()

            patient = bill.patient
            patient.status = "Completed"
            patient.save()

            BillingHistory.objects.create(
                bill=bill,
                action="Payment Success",
                description=f"Payment received Rs. {bill.total_amount}",
            )

            messages.success(request, "Payment recorded successfully.")
            return redirect("billing:receipt", payment.id)

    return render(request, "billing/payment_form.html", {"form": form, "bill": bill})


# -------------------------
# Doctor Payment History
# -------------------------
@login_required
@user_passes_test(is_doctor)
def payment_history(request):
    payments = (
        Payment.objects.select_related("bill", "bill__patient", "bill__doctor")
        .filter(bill__doctor=request.user)
        .order_by("-payment_date")
    )
    return render(request, "billing/payment_history.html", {"payments": payments})


# -------------------------
# Doctor Receipt Page
# -------------------------
@login_required
@user_passes_test(is_doctor)
def receipt(request, payment_id):
    payment = get_object_or_404(
        Payment.objects.select_related("bill", "bill__patient", "bill__doctor"),
        id=payment_id,
        bill__doctor=request.user,
    )
    return render(request, "billing/receipt.html", {"payment": payment})


# -------------------------
# Doctor Revenue Dashboard
# -------------------------
@login_required
@user_passes_test(is_doctor)
def revenue_report(request):
    payments = Payment.objects.filter(bill__doctor=request.user)
    bills = Bill.objects.filter(doctor=request.user)

    total_revenue = payments.aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
    total_payments = payments.count()
    paid_bills = bills.filter(payment_status="Paid").count()
    pending_bills = bills.filter(payment_status="Pending").count()

    return render(
        request,
        "billing/revenue_report.html",
        {
            "total_revenue": total_revenue,
            "total_payments": total_payments,
            "paid_bills": paid_bills,
            "pending_bills": pending_bills,
        },
    )


# -------------------------
# Bill Details
# -------------------------
@login_required
@user_passes_test(is_doctor)
def bill_detail(request, bill_id):
    bill = get_object_or_404(
        Bill.objects.select_related("patient", "doctor"),
        id=bill_id,
        doctor=request.user,
    )
    history = BillingHistory.objects.filter(bill=bill).order_by("-created_at")
    return render(request, "billing/bill_detail.html", {"bill": bill, "history": history})
