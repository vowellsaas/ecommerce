import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Resume, ResumeInsight
from .forms import ResumeUploadForm, ResumeCreationForm
from .ai_analysis import analyze_resume

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.employee = request.user
            resume.save()
            # Analyze the resume
            insights = analyze_resume(resume.resume_file.path)
            ResumeInsight.objects.create(resume=resume, insights=insights)
            return redirect('resume-insights', pk=resume.pk)
    else:
        form = ResumeUploadForm()
    return render(request, 'ResumeAnalyzer/upload_resume.html', {'form': form})

@login_required
def resume_insights(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    return render(request, 'ResumeAnalyzer/resume_insights.html', {'resume': resume})

@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeCreationForm(request.POST)
        if form.is_valid():
            # Generate a resume document (e.g., PDF) from the form data
            resume_path = generate_resume(form.cleaned_data)
            resume = Resume.objects.create(employee=request.user, resume_file=resume_path)
            return redirect('resume-insights', pk=resume.pk)
    else:
        form = ResumeCreationForm()
    return render(request, 'ResumeAnalyzer/create_resume.html', {'form': form})
