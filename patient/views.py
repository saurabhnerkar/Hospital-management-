from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import CustomUser
from doctor.models import Appointment
from django.utils import timezone
from django.views.decorators.http import require_POST


def is_patient(user):
    return user.role == "patient"


@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    today = timezone.now().date()

    total = Appointment.objects.filter(patient=request.user).count()
    approved = Appointment.objects.filter(patient=request.user, status__iexact="Approved").count()
    cancelled = Appointment.objects.filter(patient=request.user, status__iexact="Cancelled").count()
    upcoming = Appointment.objects.filter(
        patient=request.user,
        date__gte=today
    ).exclude(status__iexact="Cancelled").count()
    next_appointment = Appointment.objects.filter(
        patient=request.user,
        date__gte=today,
    ).exclude(status__iexact="Cancelled").order_by("date", "time").first()
    recent_appointments = Appointment.objects.select_related("doctor").filter(
        patient=request.user
    ).order_by("-date", "-time")[:5]

    context = {
        "total": total,
        "approved": approved,
        "cancelled": cancelled,
        "upcoming": upcoming,
        "next_appointment": next_appointment,
        "recent_appointments": recent_appointments,
    }

    return render(request, "patient/patient_dashboard.html", context)


@login_required
@user_passes_test(is_patient)
def book_appointment(request):
    doctors = CustomUser.objects.filter(role="doctor").order_by("first_name", "email")

    if request.method == "POST":
        doctor_id = request.POST["doctor"]
        doctor = get_object_or_404(CustomUser, id=doctor_id, role="doctor")
        today = timezone.now().date()

        try:
            appointment_date = date.fromisoformat(request.POST["date"])
        except ValueError:
            messages.error(request, "Please choose a valid appointment date.")
            return render(request, "patient/book_appointment.html", {"doctors": doctors})

        if appointment_date < today:
            messages.error(request, "Appointments can only be booked for today or a future date.")
            return render(request, "patient/book_appointment.html", {"doctors": doctors})

        Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            patient_name=request.user.first_name if request.user.first_name else request.user.email,
            patient_mobile=request.POST["mobile"],
            date=appointment_date,
            time=request.POST["time"],
            symptoms=request.POST["symptoms"],
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect("patient:appointment_history")

    return render(request, "patient/book_appointment.html", {"doctors": doctors})



@login_required
@user_passes_test(is_patient)
def appointment_history(request):
    appointments = Appointment.objects.select_related("doctor").filter(patient=request.user).order_by("-date", "-time")
    return render(
        request,
        "patient/appointment_history.html",
        {"appointments": appointments, "today": timezone.now().date()},
    )


@login_required
@user_passes_test(is_patient)
@require_POST
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    today = timezone.now().date()

    if appointment.status == "Cancelled":
        messages.info(request, "This appointment is already cancelled.")
    elif appointment.date < today:
        messages.error(request, "Only upcoming appointments can be cancelled.")
    else:
        appointment.status = "Cancelled"
        appointment.save(update_fields=["status"])
        messages.success(request, "Appointment cancelled successfully.")

    return redirect(request.POST.get("next") or "patient:appointment_history")


@login_required
@user_passes_test(is_patient)
def patient_profile(request):

    if request.method == "POST":
        request.user.first_name = request.POST["name"]
        request.user.email = request.POST["email"]
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("patient:patient_profile")

    return render(request, "patient/patient_profile.html")


@login_required
@user_passes_test(is_patient)
def patient_change_password(request):

    if request.method == "POST":
        old = request.POST["old_password"]
        new = request.POST["new_password"]

        if not request.user.check_password(old):
            messages.error(request, "Old password incorrect!")
            return redirect("patient:patient_change_password")

        request.user.set_password(new)
        request.user.save()

        messages.success(request, "Password changed successfully. Please login again.")
        return redirect("accounts:login")

    return render(request, "patient/patient_change_password.html")


@login_required
@user_passes_test(is_patient)
def appointment_report(request):
    # Show all appointments by default, ordered by most recent
    appointments = Appointment.objects.select_related("doctor").filter(
        patient=request.user
    ).order_by("-date", "-time")
    
    # If filters are applied, filter by date range
    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        if start and end:
            try:
                appointments = appointments.filter(
                    date__range=[start, end]
                ).order_by("-date", "-time")
            except:
                pass  # If date filter fails, show all
    
    context = {
        "appointments": appointments,
        "appointment_count": appointments.count()
    }
    return render(request, "patient/appointment_report.html", context)
