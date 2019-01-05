from functools import reduce
from django.db import models
from django.conf import settings

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
    slug = models.SlugField(max_length=256, unique_for_date='created')
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class QuestionVote(Vote):
    """Model for question votes"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    @property
    def votes(self):
        return reduce(lambda value, val: value+val,
                      [vote.value for vote in self.answervote_set.all()])


class Answer(Postable):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    @property
    def votes(self):
        return reduce(lambda value, val: value+val,
                      [vote.value for vote in self.answervote_set.all()])


class AnswerVote(Vote):
    """Model for answer votes"""
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
