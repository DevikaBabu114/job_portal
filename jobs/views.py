from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job
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
    
    return render(request, 'jobs/find_jobs.html', {
        'jobs': jobs,
        'search_query': search_query
    })

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

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
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

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