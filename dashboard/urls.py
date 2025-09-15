from django.urls import path
from . import views

urlpatterns = [
    path('AI_student/', views.dashboard, name='dashboard'),
    path('My_Complaint/', views.my_complaints, name='my_complaints'),
    path('New_complaint/', views.new_complaint, name='new_complaint'),
    path('complaint/<uuid:complaint_id>/', views.view_complaint, name='view_complaint'),
    path('complaint/<uuid:complaint_id>/update/', views.update_complaint, name='update_complaint'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('review/', views.review_view, name='review'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('settings/', views.settings_view, name='settings'),
    path('ai-assistant/', views.ai_assistant_view, name='ai_assistant'),
    path('track/', views.track_complaints, name='track_complaints'),
    path("new/", views.new_complaint, name="new_complaint"),
    path("my/", views.my_complaints, name="my_complaints"),
]