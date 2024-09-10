from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Resume(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    resume_file = models.FileField(upload_to='resumes/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.username} Resume'

class ResumeInsight(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='insight')
    insights = models.TextField()
    analysis_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Insights for {self.resume.employee.username}'
