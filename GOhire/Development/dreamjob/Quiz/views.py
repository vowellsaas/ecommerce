from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, QuizResult
from .forms import QuizForm
from Job.models import Job

@login_required
def take_quiz(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    quiz = Quiz.objects.filter(job=job).first()

    if not quiz:
        # If there's no quiz for the job, redirect to job details or some other page
        return redirect('job-detail', pk=job_id)

    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            score = 0
            for i, question in enumerate(questions):
                if form.cleaned_data[f'question_{i}'] == question.correct_option:
                    score += 1

            QuizResult.objects.create(employee=request.user, quiz=quiz, score=score)
            return redirect('quiz-result', job_id=job.id, quiz_id=quiz.id)

    else:
        form = QuizForm(questions=questions)

    return render(request, 'Quiz/take_quiz.html', {'form': form, 'quiz': quiz})

@login_required
def quiz_result(request, job_id, quiz_id):
    job = get_object_or_404(Job, id=job_id)
    quiz = get_object_or_404(Quiz, id=quiz_id, job=job)
    result = QuizResult.objects.filter(employee=request.user, quiz=quiz).first()

    return render(request, 'Quiz/quiz_result.html', {'quiz': quiz, 'result': result})

@login_required
def employer_view_results(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    quiz = Quiz.objects.filter(job=job).first()
    results = QuizResult.objects.filter(quiz=quiz)

    return render(request, 'Quiz/employer_view_results.html', {'quiz': quiz, 'results': results})
