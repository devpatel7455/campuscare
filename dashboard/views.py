from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Complaint, Review, CustomUser
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from .models import Notification, Complaint

# DASHBOARD
def dashboard(request):
    complaints = Complaint.objects.all().order_by('-submitted_at')[:5]  # Get the last 5 complaints
    total_complaints = Complaint.objects.count()
    ai_accuracy = 85  # Example static accuracy score

    context = {
        'complaints': complaints,
        'total_complaints': total_complaints,
        'ai_accuracy': ai_accuracy,
    }
    return render(request, 'AI_student.html', context)


def new_complaint(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        priority = request.POST.get("priority")
        location_building = request.POST.get("location_building")
        location_floor = request.POST.get("location_floor")
        location_additional = request.POST.get("location_additional")
        student_name = request.POST.get("student_name")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        anonymous = request.POST.get("anonymous") == "on"

        Complaint.objects.create(
            title=title,
            description=description,
            category=category,
            priority=priority,
            location_building=location_building,
            location_floor=location_floor,
            location_additional=location_additional,
            student_name=student_name,
            student_id=student_id,
            email=email,
            phone=phone,
            anonymous=anonymous,
        )
        return redirect("my_complaints")

    return render(request, "New_Complaint.html")


def my_complaints(request):
    complaints = Complaint.objects.all().order_by("-submitted_at")
    return render(request, "my_complaint.html", {"complaints": complaints})

# REVIEW VIEW
def review_view(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        if complaint_id and rating:
            complaint = Complaint.objects.get(id=complaint_id)
            Review.objects.create(
                complaint=complaint,
                rating=int(rating),
                text=text
            )
            return redirect('review')  # redirect after POST

    # Handle GET request or if POST data is incomplete
    complaints = Complaint.objects.filter(status='resolved')
    recent_reviews = Review.objects.order_by('-created_at')[:5]

    context = {
        'complaints': complaints,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'review.html', context)

    # Show complaints for dropdown
    


def view_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    context = {
        'complaint': complaint,
        'active_page': 'my_complaints'
    }
    return render(request, 'View_complaint.html', context)

def update_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.status = request.POST.get('status', complaint.status)
        complaint.save()
        messages.success(request, "Complaint updated successfully!")
        return redirect('my_complaints')
    context = {
        'complaint': complaint,
        'active_page': 'my_complaints'
    }
    return render(request, 'Update_complaint.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a home page
            else:
                # Return an error message
                pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to a home page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def statistics_view(request):
    # Example dummy data
    data = {
        'users_count': 100,
        'complaints_count': 50,
    }
    return render(request, 'statistics.html', data)


def notifications_view(request):
    if request.user.is_authenticated:
        # Get all notifications for the user without ordering
        notifications = Notification.objects.filter(user=request.user)
    else:
        notifications = []  # No notifications for anonymous users

    return render(request, 'notification.html', {'notifications': notifications})

def settings_view(request):
    user = request.user

    context = {
        'user': user
    }
    return render(request, 'settings.html', context)

def settings_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('firstName')
        user.last_name = request.POST.get('lastName')
        user.email = request.POST.get('email')
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone')
        profile.department = request.POST.get('department')
        profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user': user})

def ai_assistant_view(request):
    return render(request, 'ai_assistant.html', {})

def track_complaints(request):
    user = request.user
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')

    
    if status_filter != 'all':
        complaints = complaints.filter(status__iexact=status_filter)
    if search_query:
        complaints = complaints.filter(title__icontains=search_query) | complaints.filter(ticket_id__icontains=search_query)

    return render(request, 'track.html', {'track': track_complaints})