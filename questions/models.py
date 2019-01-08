from functools import reduce
from django.db import models
from django.conf import settings
from django.urls import reverse

# TODO: add tag and comment model


class TimeStampedModel(models.Model):
    """Abstract time stamped model

    It can inherited to have timestamps on the model
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class Postable(TimeStampedModel):
    """Postable model

    Abstract model for entities that can be posted
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.body


class Vote(models.Model):
    """Vote abstract model
    """
    VALUE_CHOICES = (
        (-1, -1),
        (1, 1)
    )
    voter = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    value = models.IntegerField(choices=VALUE_CHOICES)  # can only be -1 or 1

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.value}'


class Question(Postable):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    viewed = models.IntegerField(default=0)

    @property
    def url(self):
        return reverse('api:question_detail', args=[self.pk])

    @property
    def votes(self):
        vote_count = 0
        for vote in self.questionvote_set.all():
            vote_count += vote.value
        return vote_count

    def vote(self, voter, value):
        """Up votes or down votes a question
        """
        question_vote = self.questionvote_set.filter(voter=voter).first()
        if not question_vote:
            question_vote = QuestionVote(
                voter=voter, value=value, question=self)
        else:
            # TODO: edit votes
            pass
        question_vote.save()

    def mark_viewed(self):
        """Marks a question has viewed """
        self.viewed += 1
        self.save()

    def __str__(self):
        return self.title


class QuestionVote(Vote):
    """Model for question votes"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Answer(Postable):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')

    @property
    def votes(self):
        vote_count = 0
        for vote in self.answervote_set.all():
            vote_count += vote.value
        return vote_count


class AnswerVote(Vote):
    """Model for answer votes"""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
