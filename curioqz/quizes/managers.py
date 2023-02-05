from django.db import models


class QuizQueryset(models.QuerySet):
    ...


class QuizManager(models.Manager.from_queryset(QuizQueryset)):
    ...
