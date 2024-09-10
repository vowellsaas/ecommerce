from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmployerProfileForm, EmployeeProfileForm
from .models import EmployerProfile, EmployeeProfile

@login_required
def update_employer_profile(request):
    profile = request.user.employerprofile
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer-profile')  # Redirect after saving
    else:
        form = EmployerProfileForm(instance=profile)
    return render(request, 'manage_account/update_employer_profile.html', {'form': form})

@login_required
def update_employee_profile(request):
    profile = request.user.employeeprofile
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employee-profile')  # Redirect after saving
    else:
        form = EmployeeProfileForm(instance=profile)
    return render(request, 'manage_account/update_employee_profile.html', {'form': form})

# from django.shortcuts import render, redirect
# from .models import User

# def profile_view(request):
#     return render(request, 'profile.html')

# def edit_profile(request):
#     if request.method == 'POST':
#         # Logic to update profile information
#         return redirect('profile')
#     return render(request, 'edit_profile.html')
