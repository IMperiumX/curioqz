from django.db import models


class QuizQuerySet(models.QuerySet):
    pass


class QuizManager(models.Manager.from_queryset(QuizQuerySet)):
    pass
