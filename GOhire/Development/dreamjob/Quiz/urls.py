from django.urls import path
from .views import take_quiz, quiz_result, employer_view_results

urlpatterns = [
    path('<int:job_id>/take/', take_quiz, name='take-quiz'),
    path('<int:job_id>/<int:quiz_id>/result/', quiz_result, name='quiz-result'),
    path('<int:job_id>/results/', employer_view_results, name='employer-view-results'),
]
