from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import JobSeeker, Employer
import os

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def register(request):
    return render(request, 'register.html')

def register_job_seeker(request):
    form_data = {}
    errors = {}
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        location = request.POST.get('location', '').strip()
        skills = request.POST.get('skills', '').strip()
        experience = request.POST.get('experience', '').strip()
        education = request.POST.get('education', '').strip()
        bio = request.POST.get('bio', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        resume = request.FILES.get('resume')
        
        # Store form data for re-display
        form_data = {
            'username': username,
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'location': location,
            'skills': skills,
            'experience': experience,
            'education': education,
            'bio': bio,
        }
        
        # Validation
        if not username:
            errors['username'] = 'Username is required'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        
        if not full_name:
            errors['full_name'] = 'Full name is required'
        
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered'
        
        if not phone:
            errors['phone'] = 'Phone number is required'
        
        if not password1:
            errors['password1'] = 'Password is required'
        elif len(password1) < 8:
            errors['password1'] = 'Password must be at least 8 characters'
        
        if not password2:
            errors['password2'] = 'Please confirm your password'
        elif password1 != password2:
            errors['password2'] = 'Passwords do not match'
        
        # If no errors, create user and job seeker profile
        if not errors:
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=full_name
                )
                
                # Create job seeker profile
                job_seeker = JobSeeker.objects.create(
                    user=user,
                    full_name=full_name,
                    phone=phone,
                    location=location,
                    skills=skills,
                    experience=experience,
                    education=education,
                    bio=bio
                )
                
                # Handle resume file upload
                if resume:
                    job_seeker.resume = resume
                    job_seeker.save()
                
                # Log the user in
                login(request, user)
                
                # Success message
                messages.success(request, f'Welcome {full_name}! Your job seeker account has been created successfully.')
                
                # Redirect to dashboard
                return redirect('dashboard')
                
            except Exception as e:
                errors['general'] = f'An error occurred during registration: {str(e)}'
                # Clean up user if created
                if User.objects.filter(username=username).exists():
                    User.objects.filter(username=username).delete()
        
        # If there are errors, display them
        if errors:
            for field, error in errors.items():
                messages.error(request, f'{field}: {error}')
    
    # Render the form (GET request or failed POST)
    context = {
        'form_data': form_data,
        'errors': errors
    }
    return render(request, 'users/register_job_seeker.html', context)

def register_employer(request):
    form_data = {}
    errors = {}
    
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username', '').strip()
        company_name = request.POST.get('company_name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company_address = request.POST.get('company_address', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Store form data for re-display
        form_data = {
            'username': username,
            'company_name': company_name,
            'contact_person': contact_person,
            'email': email,
            'phone': phone,
            'company_address': company_address,
        }
        
        # Validation
        if not username:
            errors['username'] = 'Username is required'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        
        if not company_name:
            errors['company_name'] = 'Company name is required'
        
        if not contact_person:
            errors['contact_person'] = 'Contact person is required'
        
        if not email:
            errors['email'] = 'Email is required'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered'
        
        if not phone:
            errors['phone'] = 'Phone number is required'
        
        if not company_address:
            errors['company_address'] = 'Company address is required'
        
        if not password1:
            errors['password1'] = 'Password is required'
        elif len(password1) < 8:
            errors['password1'] = 'Password must be at least 8 characters'
        
        if not password2:
            errors['password2'] = 'Please confirm your password'
        elif password1 != password2:
            errors['password2'] = 'Passwords do not match'
        
        # If no errors, create user and employer profile
        if not errors:
            try:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email
                )
                
                # Create employer profile
                employer = Employer.objects.create(
                    user=user,
                    company_name=company_name,
                    contact_person=contact_person,
                    phone=phone,
                    company_address=company_address
                )
                
                # Log the user in
                login(request, user)
                
                # Success message
                messages.success(request, f'Welcome {contact_person}! Your employer account for {company_name} has been created successfully.')
                
                # Redirect to dashboard
                return redirect('dashboard')
                
            except Exception as e:
                errors['general'] = f'An error occurred during registration: {str(e)}'
                # Clean up user if created
                if User.objects.filter(username=username).exists():
                    User.objects.filter(username=username).delete()
        
        # If there are errors, display them
        if errors:
            for field, error in errors.items():
                messages.error(request, f'{field}: {error}')
    
    # Render the form (GET request or failed POST)
    context = {
        'form_data': form_data,
        'errors': errors
    }
    return render(request, 'register_employer.html', context)

@login_required
def dashboard(request):
    """Main dashboard - redirects based on user type"""
    try:
        # Check if user is a job seeker
        if hasattr(request.user, 'jobseeker'):
            return redirect('job_seeker_dashboard')
        # Check if user is an employer
        elif hasattr(request.user, 'employer'):
            return redirect('employer_dashboard')
        else:
            messages.error(request, 'User profile not found.')
            return redirect('home')
    except Exception as e:
        messages.error(request, 'Error accessing dashboard.')
        return redirect('home')

@login_required
def job_seeker_dashboard(request):
    """Job Seeker Dashboard"""
    try:
        job_seeker = request.user.jobseeker
        context = {
            'user': request.user,
            'job_seeker': job_seeker
        }
        return render(request, 'users/job_seeker_dashboard.html', context)
    except JobSeeker.DoesNotExist:
        messages.error(request, 'Job seeker profile not found.')
        return redirect('home')

@login_required
def update_jobseeker_profile(request):
    """Update job seeker profile - handles both AJAX and regular form submission"""
    if request.method == 'POST':
        try:
            job_seeker = request.user.jobseeker
            
            # Update job seeker fields
            job_seeker.full_name = request.POST.get('full_name', job_seeker.full_name)
            job_seeker.phone = request.POST.get('phone', job_seeker.phone)
            job_seeker.location = request.POST.get('location', job_seeker.location)
            job_seeker.skills = request.POST.get('skills', job_seeker.skills)
            job_seeker.experience = request.POST.get('experience', job_seeker.experience)
            job_seeker.education = request.POST.get('education', job_seeker.education)
            job_seeker.bio = request.POST.get('bio', job_seeker.bio)
            
            # Handle resume upload
            if 'resume' in request.FILES:
                job_seeker.resume = request.FILES['resume']
            
            job_seeker.save()
            
            # Update user email if changed
            new_email = request.POST.get('email')
            if new_email and new_email != request.user.email:
                if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
                    error_msg = 'This email is already registered with another account.'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': error_msg})
                    else:
                        messages.error(request, error_msg)
                        return redirect('job_seeker_dashboard')
                request.user.email = new_email
                request.user.save()
            
            # Update user first name if full name changed
            request.user.first_name = job_seeker.full_name
            request.user.save()
            
            # Return response based on request type
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Profile updated successfully!',
                    'data': {
                        'full_name': job_seeker.full_name,
                        'location': job_seeker.location,
                        'skills': job_seeker.skills,
                        'bio': job_seeker.bio
                    }
                })
            else:
                messages.success(request, 'Profile updated successfully!')
                return redirect('job_seeker_dashboard')
                
        except JobSeeker.DoesNotExist:
            error_msg = 'Job seeker profile not found.'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            else:
                messages.error(request, error_msg)
                return redirect('job_seeker_dashboard')
        except Exception as e:
            error_msg = f'Error updating profile: {str(e)}'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': error_msg})
            else:
                messages.error(request, error_msg)
                return redirect('job_seeker_dashboard')
    
    return redirect('job_seeker_dashboard')

@login_required
def employer_dashboard(request):
    """Employer Dashboard"""
    try:
        employer = request.user.employer
        context = {
            'user': request.user,
            'employer': employer
        }
        return render(request, 'users/employer_dashboard.html', context)
    except Employer.DoesNotExist:
        messages.error(request, 'Employer profile not found.')
        return redirect('home')