from django.urls import path
from .views import update_employer_profile, update_employee_profile


urlpatterns = [
    #   path('profile/', profile_view, name='profile'),
    # path('profile/edit/', edit_profile, name='edit-profile'),
    path('profile/employer/', update_employer_profile, name='update-employer-profile'),
    path('profile/employee/', update_employee_profile, name='update-employee-profile'),
]
