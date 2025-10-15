from django.urls import path
from . import views

urlpatterns = [
    # Job search and browsing
    path('find-jobs/', views.find_jobs, name='find_jobs'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    
    # Job application functionality
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),
    
    # Employer application management
    path('applications/', views.employer_applications, name='employer_applications'),
    path('applications/job/<int:job_id>/', views.employer_applications, name='employer_job_applications'),
    path('application/<int:application_id>/update/<str:status>/', views.update_application_status, name='update_application_status'),
    
    # Job posting and management
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('toggle-job/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
]