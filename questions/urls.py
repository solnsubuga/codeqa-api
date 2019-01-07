from django.urls import path

from .views import (QuestionDetailView, QuestionListView)

app_name = 'questions'

urlpatterns = [
    path('questions/', QuestionListView.as_view()),
    path('question/<int:pk>/', QuestionDetailView.as_view()),
]
