# from django.contrib import auth
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.shortcuts import render, redirect , get_object_or_404
# from django.urls import reverse, reverse_lazy

# from account.forms import *
# from job.permission import user_is_employee 


# def get_success_url(request):

#     """
#     Handle Success Url After LogIN

#     """
#     if 'next' in request.GET and request.GET['next'] != '':
#         return request.GET['next']
#     else:
#         return reverse('job:home')



# def employee_registration(request):

#     """
#     Handle Employee Registration

#     """
#     form = EmployeeRegistrationForm(request.POST or None)
#     if form.is_valid():
#         form = form.save()
#         return redirect('account:login')
#     context={
        
#             'form':form
#         }

#     return render(request,'account/register.html',context)


# def employer_registration(request):

#     """
#     Handle Employee Registration 

#     """

#     form = EmployerRegistrationForm(request.POST or None)
#     if form.is_valid():
#         form = form.save()
#         return redirect('account:login')
#     context={
        
#             'form':form
#         }

#     return render(request,'account/register.html',context)


# @login_required(login_url=reverse_lazy('accounts:login'))
# @user_is_employee
# def employee_edit_profile(request, id=id):

#     """
#     Handle Employee Profile Update Functionality

#     """

#     user = get_object_or_404(User, id=id)
#     form = EmployeeProfileEditForm(request.POST or None, instance=user)
#     if form.is_valid():
#         form = form.save()
#         messages.success(request, 'Your Profile Was Successfully Updated!')
#         return redirect(reverse("account:profile/update", kwargs={
#                                     'id': form.id
#                                     }))
#     context={
        
#             'form':form
#         }

#     return render(request,'account/employee-profile/update.html',context)



# def user_logIn(request):

#     """
#     Provides users to logIn

#     """

#     form = UserLoginForm(request.POST or None)
    

#     if request.user.is_authenticated:
#         return redirect('/')
    
#     else:
#         if request.method == 'POST':
#             if form.is_valid():
#                 auth.login(request, form.get_user())
#                 return HttpResponseRedirect(get_success_url(request))
#     context = {
#         'form': form,
#     }

#     return render(request,'account/login.html',context)


# def user_logOut(request):
#     """
#     Provide the ability to logout
#     """
#     auth.logout(request)
#     messages.success(request, 'You are Successfully logged out')
#     return redirect('account:login')

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserUpdateForm, EmployeeProfileForm, EmployerProfileForm, UserLoginForm
from .models import Employee, Employer
from job.permission import user_is_employee

User = get_user_model()

def get_success_url(request):
    """
    Handle Success URL After Login
    """
    if 'next' in request.GET and request.GET['next'] != '':
        return request.GET['next']
    else:
        return reverse('job:home')

def user_registration(request):
    """
    Handle User Registration (Employee or Employer)
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)

@login_required(login_url=reverse_lazy('account:login'))
def profile_update(request):
    """
    Handle Profile Update Functionality
    """
    user = request.user
    if user_is_employee:
        profile_form = EmployeeProfileForm(request.POST or None, request.FILES or None, instance=user.employee_profile)
    else:
        profile_form = EmployerProfileForm(request.POST or None, request.FILES or None, instance=user.employer_profile)
    
    user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, 'Your Profile Was Successfully Updated!')
        return redirect(reverse('account:profile_update'))
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/profile_update.html', context)

def user_login(request):
    """
    Provides users to login
    """
    if request.user.is_authenticated:
        return redirect(get_success_url(request))
    
    form = UserLoginForm(request.POST or None)

    if request.method == 'POST':
        loguname = request.POST['username']
        logpassword=request.POST['password']

        user = authenticate(username=loguname, password=logpassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'sucessfully logged in')
            return HttpResponseRedirect(get_success_url(request))
        else :
            messages.error(request, "Invalid Credentials")
            return redirect('job:home')
    
    context = {'form': form}
    return render(request, 'account/login.html', context)

def user_logout(request):
    """
    Provides the ability to logout
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('account:login')
