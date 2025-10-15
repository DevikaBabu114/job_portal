from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm

def find_jobs(request):
    # Get all active jobs
    jobs = Job.objects.filter(is_active=True)
    
    # Simple search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(employer__company_name__icontains=search_query)
        )
    
    # Check if user has applied to each job (for job seekers)
    user_has_applied = {}
    if request.user.is_authenticated and hasattr(request.user, 'jobseeker'):
        applied_job_ids = Application.objects.filter(
            job_seeker=request.user.jobseeker
        ).values_list('job_id', flat=True)
        user_has_applied = {job_id: True for job_id in applied_job_ids}
    
    return render(request, 'jobs/find_jobs.html', {
        'jobs': jobs,
        'search_query': search_query,
        'user_has_applied': user_has_applied
    })

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user has applied to this job
    has_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'jobseeker'):
        has_applied = Application.objects.filter(
            job=job, 
            job_seeker=request.user.jobseeker
        ).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })

@login_required
def apply_job(request, job_id):
    """View for job seekers to apply to a job"""
    # Check if user is a job seeker
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'Only job seekers can apply to jobs.')
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, is_active=True)
    job_seeker = request.user.jobseeker
    
    # Check if already applied
    if Application.objects.filter(job=job, job_seeker=job_seeker).exists():
        messages.warning(request, 'You have already applied to this job.')
        return redirect('job_detail', job_id=job_id)
    
    # Handle application submission
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter', '')
        
        # Create application
        Application.objects.create(
            job=job,
            job_seeker=job_seeker,
            cover_letter=cover_letter,
            status='applied'
        )
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('job_detail', job_id=job_id)
    
    return render(request, 'jobs/apply_job.html', {'job': job})

@login_required
def applied_jobs(request):
    """View for job seekers to see their applied jobs"""
    if not hasattr(request.user, 'jobseeker'):
        messages.error(request, 'Only job seekers can view applied jobs.')
        return redirect('dashboard')
    
    applications = Application.objects.filter(
        job_seeker=request.user.jobseeker
    ).select_related('job', 'job__employer').order_by('-applied_date')
    
    # Group applications by status for better organization
    applications_by_status = {
        'applied': applications.filter(status='applied'),
        'viewed': applications.filter(status='viewed'),
        'shortlisted': applications.filter(status='shortlisted'),
        'rejected': applications.filter(status='rejected'),
        'hired': applications.filter(status='hired'),
    }
    
    return render(request, 'jobs/applied_jobs.html', {
        'applications': applications,
        'applications_by_status': applications_by_status
    })

@login_required
def employer_applications(request, job_id=None):
    """View for employers to see applications for their jobs"""
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'Only employers can view applications.')
        return redirect('dashboard')
    
    employer = request.user.employer
    
    if job_id:
        # View applications for a specific job
        job = get_object_or_404(Job, id=job_id, employer=employer)
        applications = Application.objects.filter(job=job).select_related('job_seeker')
        template = 'jobs/job_applications.html'
    else:
        # View all applications across all jobs
        applications = Application.objects.filter(
            job__employer=employer
        ).select_related('job_seeker', 'job').order_by('-applied_date')
        template = 'jobs/all_applications.html'
    
    # Group applications by status
    applications_by_status = {
        'applied': applications.filter(status='applied'),
        'viewed': applications.filter(status='viewed'),
        'shortlisted': applications.filter(status='shortlisted'),
        'rejected': applications.filter(status='rejected'),
        'hired': applications.filter(status='hired'),
    }
    
    return render(request, template, {
        'applications': applications,
        'applications_by_status': applications_by_status,
        'job': job if job_id else None
    })

@login_required
def update_application_status(request, application_id, status):
    """View for employers to update application status"""
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'Only employers can update application status.')
        return redirect('dashboard')
    
    application = get_object_or_404(
        Application, 
        id=application_id, 
        job__employer=request.user.employer
    )
    
    # Validate status
    valid_statuses = dict(Application.STATUS_CHOICES).keys()
    if status not in valid_statuses:
        messages.error(request, 'Invalid status.')
        return redirect('employer_applications')
    
    # Update status
    old_status = application.status
    application.status = status
    application.save()
    
    messages.success(
        request, 
        f'Application status updated from {old_status} to {status}.'
    )
    
    # Redirect back to the appropriate page
    if request.GET.get('job_id'):
        return redirect('employer_applications', job_id=request.GET.get('job_id'))
    return redirect('employer_applications')

@login_required
def post_job(request):
    """View for employers to post new jobs"""
    # Check if user is an employer
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'Only employers can post jobs.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            # Save the job with the current employer
            job = form.save(commit=False)
            job.employer = request.user.employer
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('my_jobs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def my_jobs(request):
    """View for employers to see their posted jobs"""
    # Check if user is an employer
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'Only employers can view their jobs.')
        return redirect('dashboard')
    
    jobs = Job.objects.filter(employer=request.user.employer).order_by('-created_at')
    
    # Calculate statistics
    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    
    total_applications = 0
    pending_applications = 0
    
    # Add application counts to each job and calculate totals
    for job in jobs:
        job.application_count = Application.objects.filter(job=job).count()
        job.pending_count = Application.objects.filter(job=job, status='applied').count()
        
        total_applications += job.application_count
        pending_applications += job.pending_count
    
    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
    }
    
    return render(request, 'jobs/my_jobs.html', context)

@login_required
def edit_job(request, job_id):
    """View for employers to edit their jobs"""
    # Check if user is an employer
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'Only employers can edit jobs.')
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('my_jobs')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = JobForm(instance=job)
    
    return render(request, 'jobs/post_job.html', {'form': form, 'editing': True})

@login_required
def toggle_job_status(request, job_id):
    """View to activate/deactivate a job"""
    if not hasattr(request.user, 'employer'):
        messages.error(request, 'Only employers can manage jobs.')
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user.employer)
    job.is_active = not job.is_active
    job.save()
    
    status = "activated" if job.is_active else "deactivated"
    messages.success(request, f'Job {status} successfully!')
    return redirect('my_jobs')