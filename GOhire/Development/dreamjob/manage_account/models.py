from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import JSONField

User = get_user_model()

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    pan = models.CharField(max_length=10)
    gsttin = models.CharField(max_length=15)
    url_address = models.URLField()
    img_profile = models.ImageField(upload_to='employer_profiles/', blank=True, null=True)

    def __str__(self):
        return self.company_name

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    experiences = JSONField()
    skills = JSONField()
    resume = models.FileField(upload_to='employee_resumes/', blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
