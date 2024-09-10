from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='applications/resumes/')
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Applied', 'Applied'), ('Reviewed', 'Reviewed'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Applied')

    def __str__(self):
        return f'{self.employee.username} - {self.job.title}'
