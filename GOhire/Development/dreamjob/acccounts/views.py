from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import EmployeeSignUpForm, EmployerSignUpForm

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_employee = True
            user.save()
            login(request, user)
            return redirect('employee-dashboard')  # redirect to the employee dashboard
    else:
        form = EmployeeSignUpForm()
    return render(request, 'account/register_employee.html', {'form': form})

def register_employer(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_employer = True
            user.save()
            login(request, user)
            return redirect('employer-dashboard')  # redirect to the employer dashboard
    else:
        form = EmployerSignUpForm()
    return render(request, 'account/register_employer.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_employee:
                    return redirect('employee-dashboard')
                else:
                    return redirect('employer-dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')  # redirect to the homepage
