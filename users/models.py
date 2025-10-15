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
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.full_name
    
    @property
    def skills_list(self):
        """Convert skills string to list for display"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        return []
    
    @property
    def has_resume(self):
        """Check if resume exists"""
        return bool(self.resume)
    
    def get_experience_preview(self):
        """Get first 100 characters of experience for preview"""
        if self.experience:
            return self.experience[:100] + '...' if len(self.experience) > 100 else self.experience
        return "No experience provided"
    
    def get_education_preview(self):
        """Get first 100 characters of education for preview"""
        if self.education:
            return self.education[:100] + '...' if len(self.education) > 100 else self.education
        return "No education provided"

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    company_address = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.company_name