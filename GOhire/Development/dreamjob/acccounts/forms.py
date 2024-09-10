from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class EmployeeSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class EmployerSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
