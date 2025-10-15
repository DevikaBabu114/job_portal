from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add=True
    
    def __str__(self):
        return self.full_name

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    company_address = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # Add this too
    
    def __str__(self):
        return self.company_name