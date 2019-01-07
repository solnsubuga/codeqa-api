"""codeqaapi URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('api/v1/', include('questions.urls', namespace='api')),
]
