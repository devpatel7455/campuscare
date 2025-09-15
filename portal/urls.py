from django.urls import path
from . import views

urlpatterns = [
    path("c_admin/", views.admin_view, name="admin"),
    path("complaints/", views.complaint_list, name="complaints"),
]