# In models.py, update User model to use the custom manager
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager, EmployeeManager, EmployerManager

from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

def validate_pan(value):
    if not value.isalnum() or len(value) != 10:
        raise ValidationError("PAN must be exactly 10 alphanumeric characters.")
    if not value[:5].isalpha() or not value[5:9].isdigit() or not value[-1].isalpha():
        raise ValidationError("PAN must be in the format ABCDE1234F.")

def validate_gstin(value):
    if not value.isalnum() or len(value) != 15:
        raise ValidationError("GSTIN must be exactly 15 alphanumeric characters.")
    
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(blank=False, error_messages={'unique': "A user with that email already exists."})
    role = models.CharField(max_length=10, choices=(('employer', 'Employer'), ('employee', 'Employee')))
    gender = models.CharField(max_length=1, choices=(('M', "Male"), ('F', "Female")))
    aadhar = models.CharField(max_length=12, validators=[MinLengthValidator(12), MaxLengthValidator(12)], blank=True, null=True)
    phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', "Enter a valid 10-digit phone number.")], blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=6, validators=[RegexValidator(r'^\d{6}$', "Enter a valid 6-digit PIN code.")], blank=True, null=True)
    img = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

# In models.py, update Employee and Employer models to use their managers
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    pan = models.CharField(max_length=10, validators=[validate_pan], blank=True)
    gstin = models.CharField(max_length=15, validators=[validate_gstin], blank=True)
    company_address = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    objects = EmployerManager()

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)

    objects = EmployeeManager()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.job_title}"