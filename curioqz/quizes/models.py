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

    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    time = models.IntegerField(help_text=_("time in minutes"))
    difficulty = models.CharField(max_length=6, choices=QuizChoices.choices)
    score_to_pass = models.IntegerField(
        help_text=_(
            "required score to pass the quiz",
        )
    )

    questions = models.ManyToManyField("Question")

    def __str__(self):
        return f"{self.name} - {self.topic}"


class Category(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Question(models.Model):
    # TODO: add question app
    class QuestionChoices(models.TextChoices):
        MULTIPLE_CHOICE = "multiple-choice", "multiple-choice"
        TRUE_FALSE = "true-false", "true-false"
        FILL_IN_THE_BLANK = "fill-in-the-blank", "fill-in-the-blank"

    text = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    qtype = models.CharField(max_length=13, choices=QuestionChoices.choices)
    created = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    quiz = models.ForeignKey(
        "Quiz",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="questions",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.text)


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    questions = models.ManyToManyField("Question")

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"
