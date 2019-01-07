from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Question, Answer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class AnswerSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

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
        extra_kwargs = {
            'slug': {'allow_null': True, 'allow_blank': True, 'required': False},
        }

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, val in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, val)
        instance.save()
        return instance
