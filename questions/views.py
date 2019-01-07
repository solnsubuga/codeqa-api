from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import QuestionSerializer
from .renderers import QuestionJsonRenderer
from .models import Question, Answer


class QuestionListView(APIView):
    permission_classes = (IsAuthenticated, )
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


class QuestionDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (QuestionJsonRenderer, )
    serializer_class = QuestionSerializer

    def _get_question(self, **kwargs):
        """Helper method to get a question based on pk
        """
        try:
            question = Question.objects.get(**kwargs)
        except Question.DoesNotExist:
            raise NotFound('Question does not exist')
        return question

    def retrieve(self, request, pk, format=None, *args, **kwargs):
        question = self._get_question(pk=pk)
        serializer = self.serializer_class(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk, format=None, *args, **kwargs):
        question = self._get_question(pk=pk, author=request.user)

        data = request.data.copy()
        data.update({'slug': slugify(data.get('title'))})

        serializer = self.serializer_class(question, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk, format=None, *args, **kwargs):
        question = self._get_question(pk=pk, author=request.user)
        question.delete()
        return Response({"message": "question deleted successfully"}, status=status.HTTP_200_OK)
