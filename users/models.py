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
    
    def get_applied_jobs(self):
        """Get all jobs applied by this job seeker"""
        from jobs.models import Application  # Import here to avoid circular import
        return Application.objects.filter(job_seeker=self).select_related('job')
    
    def get_applications_by_status(self, status):
        """Get applications by status"""
        from jobs.models import Application
        return Application.objects.filter(job_seeker=self, status=status)
    
    def has_applied_to_job(self, job):
        """Check if job seeker has applied to a specific job"""
        from jobs.models import Application
        return Application.objects.filter(job_seeker=self, job=job).exists()
    
    @property
    def skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',') if skill.strip()]
        return []
    
    @property
    def has_resume(self):
        return bool(self.resume)
    
    def get_experience_preview(self):
        if self.experience:
            return self.experience[:100] + '...' if len(self.experience) > 100 else self.experience
        return "No experience provided"
    
    def get_education_preview(self):
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
    
    def get_posted_jobs(self):
        """Get all jobs posted by this employer"""
        from jobs.models import Job
        return Job.objects.filter(employer=self)
    
    def get_active_jobs(self):
        """Get active jobs posted by this employer"""
        from jobs.models import Job
        return Job.objects.filter(employer=self, is_active=True)
    
    def get_job_applications(self, job=None):
        """Get all applications for employer's jobs"""
        from jobs.models import Application
        if job:
            return Application.objects.filter(job=job).select_related('job_seeker', 'job')
        return Application.objects.filter(job__employer=self).select_related('job_seeker', 'job')
    
    def get_applications_count(self):
        """Get total applications across all jobs"""
        from jobs.models import Application
        return Application.objects.filter(job__employer=self).count()
    
    def get_pending_applications_count(self):
        """Get pending applications across all jobs"""
        from jobs.models import Application
        return Application.objects.filter(job__employer=self, status='applied').count()