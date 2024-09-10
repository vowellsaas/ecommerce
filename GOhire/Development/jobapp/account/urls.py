from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # User Registration
    path('register/', views.user_registration, name='register'),
    
    # Profile Update
    path('profile_update/', views.profile_update, name='profile_update'),
    
    # User Login
    path('login/', views.user_login, name='login'),
    
    # User Logout
    path('logout/', views.user_logout, name='logout'),
]
