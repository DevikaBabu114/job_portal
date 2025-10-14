from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobSeeker, Employer

class JobSeekerRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            JobSeeker.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                phone=self.cleaned_data['phone']
            )
        return user

class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    contact_person = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    company_address = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'company_name', 'contact_person', 'email', 'phone', 'company_address', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Employer.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                contact_person=self.cleaned_data['contact_person'],
                phone=self.cleaned_data['phone'],
                company_address=self.cleaned_data['company_address']
            )
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)