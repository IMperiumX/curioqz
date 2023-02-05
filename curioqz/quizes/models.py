from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from curioqz.quizes.managers import QuizManager
from curioqz.quizes.models_mixins import QuizMixin

User = get_user_model()


class Quiz(QuizMixin, models.Model):
    class QuizChoices(models.TextChoices):
        EASY = "easy", "easy"
        MEDIUM = "medium", "medium"
        HARD = "hard", "hard"

    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    intro = models.TextField(blank=True, null=True)
    introformat = models.CharField(max_length=10, default="html")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    time_open = models.DateTimeField(blank=True, null=True)
    time_close = models.DateTimeField(blank=True, null=True)
    time_limit = models.IntegerField(help_text=_("time in minutes"))

    grade_method = models.CharField(max_length=10, default="highest")
    decimal_points = models.DecimalField(max_digits=3, decimal_places=0)
    question_per_page = models.IntegerField(default=0)

    difficulty = models.CharField(max_length=6, choices=QuizChoices.choices)
    score_to_pass = models.IntegerField(
        help_text=_(
            "required score to pass the quiz",
        )
    )
    delay1 = models.IntegerField()
    delay2 = models.IntegerField()

    show_user_picture = models.BooleanField(default=False)
    show_blocks = models.BooleanField(default=False)
    shuffle_questions = models.BooleanField(default=False)
    shuffle_answers = models.BooleanField(default=False)

    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    review = models.ForeignKey("Review", on_delete=models.CASCADE)

    objects = QuizManager()

    class Meta:
        verbose_name_plural = _("quizes")

    def __str__(self):
        return f"{self.name} - {self.topic}"


class Review(models.Model):
    title = models.CharField(max_length=255)
    marks = models.IntegerField(default=0)
    right_answer = models.IntegerField(default=0)
    correctness = models.IntegerField(default=0)
    specific_feedback = models.TextField(blank=True, null=True)
    general_feedback = models.TextField(blank=True, null=True)
    overall_feedback = models.TextField(blank=True, null=True)

    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def __str__(self):
        return f"{self.title} - {self.marks}"


class Attempt(models.Model):
    slug = models.SlugField(default=uuid4, unique=True)

    start = models.DateTimeField(auto_now=True)
    finish = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    preview = models.IntegerField(default=0)

    quiz = models.ForeignKey(
        "Quiz",
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attempts",
    )


class Grade(models.Model):
    grade = models.DecimalField(max_digits=3, decimal_places=0)


class QuizGrade(models.Model):
    quiz = models.ForeignKey(
        "Quiz",
        on_delete=models.CASCADE,
        related_name="quiz_grades",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_grades",
    )
    grade = models.ForeignKey(
        "Grade",
        on_delete=models.CASCADE,
        related_name="quiz_grades",
    )

    modified = models.DateTimeField(auto_now=True)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        "Quiz",
        on_delete=models.CASCADE,
        related_name="quiz_questions",
    )

    questions = models.ForeignKey(
        "questions.Question",
        on_delete=models.CASCADE,
        related_name="quiz_questions",
    )


# TODO: add quiz reports
