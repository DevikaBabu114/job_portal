from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 
            'department', 
            'location', 
            'job_type', 
            'experience_level', 
            'salary', 
            'description', 
            'requirements'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter detailed job description...'
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'List the requirements and qualifications...'
            }),
            'salary': forms.TextInput(attrs={
                'placeholder': 'e.g., $50,000 - $70,000 per year'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., Senior Software Engineer'
            }),
            'department': forms.TextInput(attrs={
                'placeholder': 'e.g., Engineering, Marketing, Sales'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g., New York, NY or Remote'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Make certain fields required
        self.fields['title'].required = True
        self.fields['department'].required = True
        self.fields['location'].required = True
        self.fields['job_type'].required = True
        self.fields['experience_level'].required = True
        self.fields['description'].required = True
        self.fields['requirements'].required = True