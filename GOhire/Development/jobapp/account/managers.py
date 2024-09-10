from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class EmployeeManager(models.Manager):
    def get_by_natural_key(self, user):
        return self.get(user=user)

    def get_employees_by_department(self, department):
        return self.filter(department=department)

class EmployerManager(models.Manager):
    def get_by_natural_key(self, user):
        return self.get(user=user)

    def get_employers_by_company_name(self, company_name):
        return self.filter(company_name__icontains=company_name)