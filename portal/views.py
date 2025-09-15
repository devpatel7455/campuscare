from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Complaint
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model   


# Create your views here.

User = get_user_model()

def admin_view(request):
    complaints = Complaint.objects.all().order_by("-submitted_at")
    total_complaints = complaints.count()
    pending_complaints = complaints.filter(status='pending').count()
    resolved_complaints = complaints.filter(status='resolved').count()

    context = {
        "total_complaints": total_complaints,
        "pending_complaints": pending_complaints,
        "resolved_complaints": resolved_complaints,
    }
    return render(request, "admin.html", context)


def complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    users = User.objects.all()
    return render(request, "complaint.html", {
        "complaints": complaints,
        "users": users,
    })


def c_complaint(request):
    complaints = Complaint.objects.all().select_related("assigned_to")
    users = User.objects.all()

    return render(request, "complaint.html", {   # ✅ corrected filename
        "complaints": complaints,
        "users": users,
    })

def all_complaints(request):
    complaints = Complaint.objects.all().order_by("-submitted_at")
    return render(request, "complaint.html", {"complaints": complaints})
