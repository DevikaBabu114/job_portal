# your_app/admin.py

from django.contrib import admin
from .models import JobSeeker, Employer

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'location', 'created_at')
    search_fields = ('full_name', 'phone', 'location')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'phone', 'is_verified', 'created_at')
    search_fields = ('company_name', 'contact_person')
