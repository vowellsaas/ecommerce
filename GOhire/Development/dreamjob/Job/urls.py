from django.urls import path
from .views import dashboard,home,create_job, job_list, job_detail, apply_for_job, employee_applications, employer_job_applications

urlpatterns = [
#     path('', job_list, name='job-list'),
    path('', home, name='home'),
    path('job/<int:pk>/', job_detail, name='job-detail'),
    path('job/create/', create_job, name='create-job'),
    path('job/dashboard/', dashboard, name='dashboard'),
    path('job/<int:pk>/apply/', apply_for_job, name='apply-for-job'),
    path('applications/', employee_applications, name='employee-applications'),
    path('job/<int:pk>/applications/', employer_job_applications, name='employer-job-applications'),
]
