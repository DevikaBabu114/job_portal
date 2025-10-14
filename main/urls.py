from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/jobseeker/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('dashboard/employer/', views.employer_dashboard, name='employer_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]