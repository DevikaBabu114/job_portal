from django.contrib.auth.models import User
from django.db import models

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    
    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
    )
    
    employer = models.ForeignKey('users.Employer', on_delete=models.CASCADE)  # Use string reference
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    salary = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_applications_count(self):
        """Get total applications for this job"""
        return self.application_set.count()
    
    def get_pending_applications_count(self):
        """Get pending applications for this job"""
        return self.application_set.filter(status='applied').count()
    
    class Meta:
        ordering = ['-created_at']

class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job_seeker = models.ForeignKey('users.JobSeeker', on_delete=models.CASCADE)  # Use string reference
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.job_seeker} - {self.job}"
    
    def is_pending(self):
        return self.status == 'applied'
    
    def is_accepted(self):
        return self.status in ['shortlisted', 'hired']
    
    def is_rejected(self):
        return self.status == 'rejected'
    
    class Meta:
        unique_together = ['job_seeker', 'job']
        ordering = ['-applied_date']