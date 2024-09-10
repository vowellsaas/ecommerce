from django.urls import path
from .views import upload_resume, resume_insights, create_resume

urlpatterns = [
    path('upload/', upload_resume, name='upload-resume'),
    path('insights/<int:pk>/', resume_insights, name='resume-insights'),
    path('create/', create_resume, name='create-resume'),
]
