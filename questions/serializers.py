from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Answer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class AnswerSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'body', 'author', 'votes', 'created', 'updated']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'slug', 'answers',
                  'created', 'updated', 'viewed', 'votes', 'author']
