from django.db import models
from django.contrib.auth import get_user_model
from Job.models import Job  # Assuming you have a Job model in the Job app

User = get_user_model()

class Quiz(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class QuizResult(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee.username} - {self.quiz.title} - {self.score}'
