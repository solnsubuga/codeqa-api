from django.shortcuts import get_object_or_404, get_list_or_404
from django.template.defaultfilters import slugify
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .serializers import QuestionSerializer, AnswerSerializer
from .renderers import QuestionJsonRenderer
from .models import Question, Answer


def get_question(**kwargs):
    """Helper method to get a question based on pk
    """
    try:
        question = Question.objects.get(**kwargs)
    except Question.DoesNotExist:
        raise NotFound('Question does not exist')
    return question


class ListCreateQuestionView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (QuestionJsonRenderer, )
    serializer_class = QuestionSerializer

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data.update({'slug': slugify(data.get('title'))})
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyQuestionView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (QuestionJsonRenderer, )
    serializer_class = QuestionSerializer

    def retrieve(self, request, pk, format=None, *args, **kwargs):
        question = get_question(pk=pk)
        serializer = self.serializer_class(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk, format=None, *args, **kwargs):
        question = get_question(pk=pk, author=request.user)

        data = request.data.copy()
        data.update({'slug': slugify(data.get('title'))})

        serializer = self.serializer_class(question, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk, format=None, *args, **kwargs):
        question = get_question(pk=pk, author=request.user)
        question.delete()
        return Response({"message": "question deleted successfully"}, status=status.HTTP_200_OK)


class RetrieveUpdateDestroyAnswerView(RetrieveUpdateDestroyAPIView):
    """Handles retrieve, updating and destroy an answer for a question
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    renderer_classes = (QuestionJsonRenderer, )

    def get_object(self):
        question = get_question(pk=self.kwargs.get('question_pk'))
        try:
            answer = Answer.objects.get(
                pk=self.kwargs.get('pk'), question_id=question.id)
        except Answer.DoesNotExist:
            raise NotFound('Answer does not exist')
        return answer

    def perform_update(self, serializer):
        answer = self.get_object()
        if answer.author != self.request.user:
            raise NotAcceptable('You can edit an answer by another author')
        serializer.save()


class ListCreateAnswerView(ListCreateAPIView):
    """Handles listing and creating answers for a question
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    renderer_classes = (QuestionJsonRenderer, )

    def get_queryset(self):
        """ Filter to return answers belonging to a given question """
        question_id = self.kwargs.get('question_pk')
        question = get_question(pk=question_id)
        return question.answers

    def perform_create(self, serializer):
        question = get_question(pk=self.kwargs.get('question_pk'))
        serializer.save(question=question, author=self.request.user)
