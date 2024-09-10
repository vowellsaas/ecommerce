from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from account.models import User


class EmployeeRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name:"
        self.fields['last_name'].label = "Last Name:"
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Confirm Password:"
        self.fields['email'].label = "Email:"
        self.fields['gender'].label = "Gender:"

        # Adding placeholders
        for field in self.fields:
            placeholder = f"Enter {self.fields[field].label.split(':')[0]}"
            self.fields[field].widget.attrs.update({'placeholder': placeholder})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required.")
        return gender

    def save(self, commit=True):
        user = super(EmployeeRegistrationForm, self).save(commit=False)
        user.role = "employee"
        if commit:
            user.save()
        return user


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].label = "Company Name:"
        self.fields['last_name'].label = "Company Address:"
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Confirm Password:"

        # Adding placeholders
        for field in self.fields:
            placeholder = f"Enter {self.fields[field].label.split(':')[0]}"
            self.fields[field].widget.attrs.update({'placeholder': placeholder})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(EmployerRegistrationForm, self).save(commit=False)
        user.role = "employer"
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            if not self.user:
                raise forms.ValidationError("Invalid email or password.")
            if not self.user.is_active:
                raise forms.ValidationError("This account is inactive.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user


class EmployeeProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender"]
