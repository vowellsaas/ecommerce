from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import EmployerProfile, EmployeeProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_employer:
            EmployerProfile.objects.create(user=instance)
        elif instance.is_employee:
            EmployeeProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_employer:
        instance.employerprofile.save()
    elif instance.is_employee:
        instance.employeeprofile.save()
