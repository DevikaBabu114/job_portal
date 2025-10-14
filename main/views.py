from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    # For now, use dummy data since the database might not be ready
    stats = {
        'active_jobs': 0,
        'companies': 0,
        'candidates': 0,
    }
    
    recent_jobs = []
    
    return render(request, 'main/home.html', {
        'stats': stats,
        'recent_jobs': recent_jobs
    })

@login_required
def dashboard(request):
    # Simple dashboard view for now
    # We'll enhance this later based on user type
    context = {
        'username': request.user.username
    }
    return render(request, 'main/dashboard.html', context)

# Add these placeholder views for different dashboard types
@login_required
def jobseeker_dashboard(request):
    context = {
        'username': request.user.username,
        'user_type': 'Job Seeker'
    }
    return render(request, 'main/jobseeker_dashboard.html', context)

@login_required
def employer_dashboard(request):
    context = {
        'username': request.user.username,
        'user_type': 'Employer'
    }
    return render(request, 'main/employer_dashboard.html', context)

@login_required
def admin_dashboard(request):
    context = {
        'username': request.user.username,
        'user_type': 'Admin'
    }
    return render(request, 'main/admin_dashboard.html', context)