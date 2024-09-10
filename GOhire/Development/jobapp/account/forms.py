from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Employee, Employer

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    
    user_type = forms.ChoiceField(
        choices=[('employee', 'Employee'), ('employer', 'Employer')],
        label="Register as",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'gender', 'aadhar', 'phone', 'address', 'city', 'pin_code', 'img')
        widgets={'user_type'}
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')
        if commit:
            user.save()
            if user_type == 'employee':
                Employee.objects.create(user=user)
            elif user_type == 'employer':
                Employer.objects.create(user=user)
        return user

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'aadhar', 'phone', 'address', 'city', 'pin_code', 'img')

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name', 'pan', 'gstin', 'company_address', 'url')

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('job_title', 'department', 'experience', 'resume', 'skills', 'portfolio')

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
