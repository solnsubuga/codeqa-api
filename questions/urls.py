from django.urls import path

from .views import (RetrieveUpdateDestroyQuestionView, ListCreateQuestionView,
                    RetrieveUpdateDestroyAnswerView, ListCreateAnswerView)

app_name = 'questions'

urlpatterns = [
    path('questions/', ListCreateQuestionView.as_view(), name='question_list'),
    path('question/<int:pk>/',
         RetrieveUpdateDestroyQuestionView.as_view(), name='question_detail'),

    path('question/<int:question_pk>/answers/',
         ListCreateAnswerView.as_view(), name='answer_list'),

    path('question/<int:question_pk>/answers/<int:pk>',
         RetrieveUpdateDestroyAnswerView.as_view(), name='answer_detail'),

]
