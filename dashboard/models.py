from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.conf import settings
from django.contrib import admin
import uuid

# Custom user model
class CustomUser(AbstractUser):
    # Add any additional fields you need
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.email


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending Review'),
        ('resolved', 'Resolved'),
    ]

    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('management', 'Management'),
        ('facilities', 'Facilities'),
        ('it', 'IT'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    complaint_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location_building = models.CharField(max_length=255, blank=True, null=True)
    location_floor = models.CharField(max_length=255, blank=True, null=True)
    location_additional = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    anonymous = models.BooleanField(default=False)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(default=timezone.now)

    # 🔑 NEW: Assign complaints to staff/admin
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dashboard_assigned_complaints"
    )

    def __str__(self):
        return self.title


# Review model
class Review(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.complaint.title}"

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('ai', 'AI Suggestion'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    description = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({'Read' if self.is_read else 'Unread'})"

class track(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    progress = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
