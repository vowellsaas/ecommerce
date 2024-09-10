
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    # Add more fields later as needed
