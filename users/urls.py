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
    
   # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/job-seeker/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('profile/update/', views.update_jobseeker_profile, name='update_jobseeker_profile'),
]