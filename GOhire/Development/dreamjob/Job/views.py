from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm

from django.shortcuts import render
from .models import Job

def home(request):
    jobs = Job.objects.all()
    return render(request, 'home.html', {'jobs': jobs})

@login_required
def create_job(request):
    if request.user.is_employer:
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.employer = request.user
                job.save()
                return redirect('job-list')
        else:
            form = JobForm()
        return render(request, 'Job/create_job.html', {'form': form})
    else:
        return redirect('home')

def job_list(request):
    jobs = Job.objects.all().order_by('-date_posted')
    return render(request, 'Job/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'Job/job_detail.html', {'job': job})

@login_required
def apply_for_job(request, pk=id):
    job = get_object_or_404(Job, pk=pk)
    if request.user.is_employee:
        if request.method == 'POST':
            form = JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.employee = request.user
                application.job = job
                application.save()
                return redirect('job-detail', pk=job.pk)
        else:
            form = JobApplicationForm()
        return render(request, 'Job/apply_for_job.html', {'form': form, 'job': job})
    else:
        return redirect('home')

@login_required
def employee_applications(request):
    applications = request.user.applications.all()
    return render(request, 'Job/employee_applications.html', {'applications': applications})

@login_required
def employer_job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.user == job.employer:
        applications = job.applications.all()
        return render(request, 'Job/employer_job_applications.html', {'applications': applications, 'job': job})
    else:
        return redirect('home')

from django.shortcuts import render
from .models import Job

def dashboard(request):
    jobs = Job.objects.filter(company=request.user.profile.company_name)
    return render(request, 'dashboard.html', {'jobs': jobs})
