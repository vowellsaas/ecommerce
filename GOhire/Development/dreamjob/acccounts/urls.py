from django.urls import path
from .views import register_employee, register_employer, login_user, logout_user

urlpatterns = [
    path('register/employee/', register_employee, name='register-employee'),
    path('register/employer/', register_employer, name='register-employer'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
