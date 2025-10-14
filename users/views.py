from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import JobSeeker, Employer

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
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
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST['username']
            password = request.POST['password']
            full_name = request.POST['full_name']
            email = request.POST['email']
            phone = request.POST['phone']
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'register_job_seeker.html')
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered. Please use a different email.')
                return render(request, 'register_job_seeker.html')
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=full_name
            )
            
            # Create job seeker profile
            JobSeeker.objects.create(
                user=user,
                full_name=full_name,
                phone=phone
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {full_name}!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'register_job_seeker.html')

def register_employer(request):
    if request.method == 'POST':
        try:
            # Get form data
            username = request.POST['username']
            password = request.POST['password']
            company_name = request.POST['company_name']
            contact_person = request.POST['contact_person']
            email = request.POST['email']
            phone = request.POST['phone']
            company_address = request.POST['company_address']
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return render(request, 'register_employer.html')
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered. Please use a different email.')
                return render(request, 'register_employer.html')
            
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=contact_person
            )
            
            # Create employer profile
            Employer.objects.create(
                user=user,
                company_name=company_name,
                contact_person=contact_person,
                phone=phone,
                company_address=company_address
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Employer account created successfully! Welcome, {company_name}!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating employer account: {str(e)}')
    
    return render(request, 'register_employer.html')