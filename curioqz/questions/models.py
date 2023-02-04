from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Question(models.Model):
    class QuestionChoices(models.TextChoices):
        MULTIPLE_CHOICE = "multiple-choice", "multiple-choice"
        TRUE_FALSE = "true-false", "true-false"
        FILL_IN_THE_BLANK = "fill-in-the-blank", "fill-in-the-blank"

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    type = models.CharField(max_length=13, choices=QuestionChoices.choices)
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
    answers = models.ManyToManyField("Answer")

    def __str__(self):
        return str(self.text)


class Category(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    info = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Answer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class CorrectAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.answer.text}"
