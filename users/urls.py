from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Authentication URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Registration URLs
    path('register/job-seeker/', views.register_job_seeker, name='register_job_seeker'),
    path('register/employer/', views.register_employer, name='register_employer'),
    
    # Dashboard URL (temporary - we'll create the view later)
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]