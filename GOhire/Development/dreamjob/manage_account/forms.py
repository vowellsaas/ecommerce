from django import forms
from .models import EmployerProfile, EmployeeProfile

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'email', 'pan', 'gsttin', 'url_address', 'img_profile']

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['experiences', 'skills', 'resume', 'portfolio']
