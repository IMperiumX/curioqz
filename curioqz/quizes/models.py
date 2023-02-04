from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Quiz(models.Model):
    # TODO: link with courses app
    class QuizChoices(models.TextChoices):
        EASY = "easy", "easy"
        MEDIUM = "medium", "medium"
        HARD = "hard", "hard"

    name = models.CharField(max_length=255)
    intro = models.TextField(blank=True, null=True)
    introformat = models.CharField(max_length=10, default="html")
    time_open = models.DateTimeField(blank=True, null=True)
    time_close = models.DateTimeField(blank=True, null=True)
    attempts = models.IntegerField(default=0)
    attempt_on_last = models.BooleanField(default=False)
    grade_method = models.CharField(max_length=10, default="highest")
    decimal_points = models.DecimalField(max_digits=3, decimal_places=0)
    review_attempt = models.IntegerField(default=0)
    review_correctness = models.IntegerField(default=0)
    review_marks = models.IntegerField(default=0)
    review_specific_feedback = models.IntegerField(default=0)
    review_general_feedback = models.IntegerField(default=0)
    review_right_answer = models.IntegerField(default=0)
    review_overall_feedback = models.IntegerField(default=0)
    question_per_page = models.IntegerField(default=0)
    shuffle_questions = models.BooleanField(default=False)
    shuffle_answers = models.BooleanField(default=False)
    # TODO: add FK to Grade, and QuizAttempt models
    topic = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    time_limit = models.IntegerField(help_text=_("time in minutes"))

    difficulty = models.CharField(max_length=6, choices=QuizChoices.choices)
    score_to_pass = models.IntegerField(
        help_text=_(
            "required score to pass the quiz",
        )
    )
    delay1 = models.IntegerField(
        help_text=_(
            "delay between attempts in minutes",
        )
    )

    delay2 = models.IntegerField(
        help_text=_(
            "delay between attempts in minutes",
        )
    )
    show_user_picture = models.BooleanField(default=False)
    show_blocks = models.BooleanField(default=False)

    questions = models.ManyToManyField("Question")

    def __str__(self):
        return f"{self.name} - {self.topic}"
