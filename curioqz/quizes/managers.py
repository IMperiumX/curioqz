from django.db import models


class QuizQuerySet(models.QuerySet):
    pass


class QuizManager(models.Manager.from_queryset(QuizQuerySet)):
    pass


class QuizQustionsQuerySet(models.QuerySet):
    pass


class QuizQuestionsManager(models.Manager.from_queryset(QuizQustionsQuerySet)):
    pass
