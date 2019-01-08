from unittest import TestCase
from django.contrib.auth.models import User
from autofixture import AutoFixture

from questions.models import (Question, QuestionVote, Answer, AnswerVote)


class TestModelsTestCase(TestCase):
    def setUp(self):
        self.username = 'myuser'
        self.password = 'password'
        self.user = User.objects.create_user(
            self.username, 'myuser@example.com', self.password)

        self.question = AutoFixture(Question, field_values={
            'author': self.user
        }).create(1)[0]

    def test_question_can_be_voted(self):
        pass

    def test_can_get_question_votes(self):
        self.assertGreaterEqual(self.question.votes, 0)

    def test_question_has_string_representation(self):
        self.assertEqual(
            f'<Question: {self.question.title}>', repr(self.question))

    def test_mark_viewed_marks_viewed(self):
        self.question.mark_viewed()
        self.assertEqual(self.question.viewed, 1)

    def tearDown(self):
        user = User.objects.filter(username=self.username).first()
        if user:
            user.delete()
