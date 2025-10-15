from django.urls import path
from . import views

urlpatterns = [
    # Job search and browsing
    path('find-jobs/', views.find_jobs, name='find_jobs'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    
    # Job posting and management
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('toggle-job/<int:job_id>/', views.toggle_job_status, name='toggle_job_status'),
]