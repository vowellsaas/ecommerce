from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job.urls', namespace='job')),   # Home or base URLs
    path('account/', include('account.urls', namespace='account')),  # Account-related URLs
    path('__debug__/', include('debug_toolbar.urls')),  # Debug toolbar URLs
]
