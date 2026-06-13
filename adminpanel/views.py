from pathlib import Path

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from accounts.models import CustomUser, Specialization
from doctor.models import Appointment, AddedPatient
from django.db.models import Q
from django.utils import timezone


HOMEPAGE_CONTENT_PATH = Path(settings.BASE_DIR) / "homepage_content.txt"



def is_admin(user):
    return user.role == "admin"


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    total_doctors = CustomUser.objects.filter(role="doctor").count()
    total_specializations = Specialization.objects.count()
    total_patients = CustomUser.objects.filter(role="patient").count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status__iexact="Pending").count()
    approved_appointments = Appointment.objects.filter(status__iexact="Approved").count()
    recent_appointments = Appointment.objects.select_related("doctor", "patient").order_by("-created_at")[:6]

    context = {
        "total_doctors": total_doctors,
        "total_specializations": total_specializations,
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
        "approved_appointments": approved_appointments,
        "recent_appointments": recent_appointments,
    }

    return render(request,"adminpanel/admin_dashboard.html", context)


@login_required
@user_passes_test(is_admin)
def doctors_list(request):
    doctors = CustomUser.objects.filter(role="doctor").order_by("email")
    return render(request, "adminpanel/doctors_list.html", {"doctors": doctors})


@login_required
@user_passes_test(is_admin)
def doctor_profile(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk, role="doctor")
    return render(request, "adminpanel/doctor_profile.html", {"doctor": doctor})


@login_required
@user_passes_test(is_admin)
def doctor_appointments(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk)
    appointments = Appointment.objects.filter(doctor=doctor).order_by("-date", "-time")
    return render(request, "adminpanel/doctor_appointments.html", {"appointments": appointments})


@login_required
@user_passes_test(is_admin)
def doctor_patients(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk)
    patients = AddedPatient.objects.filter(doctor=doctor).order_by("-created_at")
    return render(request, "adminpanel/doctor_patients.html", {"patients": patients})


@login_required
@user_passes_test(is_admin)
def registered_users(request):
    users = Appointment.objects.values("patient__email", "patient__id").distinct().order_by("patient__email")
    return render(request, "adminpanel/registered_users.html", {"users": users})


@login_required
@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    messages.success(request, "User deleted!")
    return redirect("adminpanel:registered_users")


@login_required
@user_passes_test(is_admin)
def patients_list(request):
    patients = CustomUser.objects.filter(role="patient").order_by("email")
    return render(request, "adminpanel/patients_list.html", {"patients": patients})


@login_required
@user_passes_test(is_admin)
def delete_patient(request, pk):
    patient = get_object_or_404(CustomUser, pk=pk, role="patient")
    patient.delete()
    messages.success(request, "Patient deleted!")
    return redirect("adminpanel:patients_list")


@login_required
@user_passes_test(is_admin)
def appointment_history(request):
    appointments = Appointment.objects.all().order_by("-date", "-time")
    return render(request, "adminpanel/appointment_history.html", {"appointments": appointments})


@login_required
@user_passes_test(is_admin)
def search_doctor(request):
    query = request.GET.get("q", "")

    doctors = CustomUser.objects.filter(role="doctor").filter(
        Q(first_name__icontains=query) |
        Q(email__icontains=query)
    ).order_by("email")

    return render(request, "adminpanel/search_doctor.html", {"doctors": doctors, "query": query})


@login_required
@user_passes_test(is_admin)
def search_patient(request):
    query = request.GET.get("q", "")

    patients = CustomUser.objects.filter(role="patient").filter(
        Q(first_name__icontains=query) |
        Q(email__icontains=query)
    ).order_by("email")

    return render(request, "adminpanel/search_patient.html", {"patients": patients, "query": query})


@login_required
@user_passes_test(is_admin)
def doctor_report(request):

    doctors = CustomUser.objects.filter(role="doctor")
    reports = []

    if request.method == "POST":
        doctor_id = request.POST["doctor"]
        start = request.POST["start"]
        end = request.POST["end"]

        reports = Appointment.objects.filter(
            doctor_id=doctor_id,
            date__range=[start, end]
        ).order_by("date", "time")

    return render(request, "adminpanel/doctor_report.html", {
        "doctors": doctors,
        "reports": reports,
    })


@login_required
@user_passes_test(is_admin)
def webpage_update(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        HOMEPAGE_CONTENT_PATH.write_text(content, encoding="utf-8")
        messages.success(request, "Webpage updated successfully!")
        return redirect("adminpanel:webpage_update")

    try:
        content = HOMEPAGE_CONTENT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        content = ""

    return render(request, "adminpanel/webpage_update.html", {"content": content})


@login_required
@user_passes_test(is_admin)
def admin_profile(request):

    if request.method == "POST":
        request.user.email = request.POST["email"]
        request.user.save()

        messages.success(request, "Profile updated!")
        return redirect("adminpanel:admin_profile")

    return render(request, "adminpanel/admin_profile.html")


@login_required
@user_passes_test(is_admin)
def admin_change_password(request):

    if request.method == "POST":
        old = request.POST["old_password"]
        new = request.POST["new_password"]

        if not request.user.check_password(old):
            messages.error(request, "Old password incorrect!")
            return redirect("adminpanel:admin_change_password")

        request.user.set_password(new)
        request.user.save()

        messages.success(request, "Password changed! Login again.")
        return redirect("accounts:login")

    return render(request, "adminpanel/admin_change_password.html")
