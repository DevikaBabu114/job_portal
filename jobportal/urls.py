"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Main app URLs
    path('', include('main.urls')),
    
    # User authentication and dashboard URLs
    path('users/', include('users.urls')),
    
    # Jobs and applications URLs
    path('jobs/', include('jobs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)