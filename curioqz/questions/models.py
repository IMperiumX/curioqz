from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


#####################
#                   #
#   Question Bank   #
#                   #
#####################


class Question(models.Model):
    class QuestionChoices(models.TextChoices):
        # TODO: rework questions types
        MULTIPLE_CHOICE = "multiple-choice", "multiple-choice"
        TRUE_FALSE = "true-false", "true-false"
        FILL_IN_THE_BLANK = "fill-in-the-blank", "fill-in-the-blank"

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    type = models.CharField(max_length=20, choices=QuestionChoices.choices)
    created = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)

    general_feedback = models.TextField()
    default_grade = models.DecimalField(max_digits=3, decimal_places=0)
    penalty = models.DecimalField(max_digits=3, decimal_places=0)

    created_by = models.ForeignKey(
        User,  # TODO: alter with schools(app) Prof Model
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
    text = models.TextField()
    correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"answer: {self.text}, correct: {self.correct}"


class Cagtegory(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QuestionAnswer(models.Model):
    fraction = models.DecimalField(max_digits=3, decimal_places=0)

    answer = models.TextField()
    feedback = models.TextField()

    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="question_answers",
    )


#####################
#                   #
#  Question Engine  #
#                   #
#####################


class QuestionSession(models.Model):
    newest = models.IntegerField(default=0)
    new_graded = models.IntegerField(default=0)
    sum_penalty = models.DecimalField(max_digits=3, decimal_places=0)
    comment = models.TextField()

    flagged = models.BooleanField(default=False)

    attempt = models.ForeignKey(
        "Attempt",
        on_delete=models.CASCADE,
        related_name="question_sessions",
    )
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="questions_sessions",
    )


class State(models.Model):
    answer = models.TextField()
    seq_number = models.IntegerField(default=0)

    event = models.IntegerField(default=0)
    grade = models.DecimalField(max_digits=3, decimal_places=0)
    raw_grade = models.DecimalField(max_digits=4, decimal_places=0)
    penlity = models.DecimalField(max_digits=3, decimal_places=0)

    attempt = models.ForeignKey(
        "Attempt",
        on_delete=models.CASCADE,
        related_name="question_states",
    )
    question = models.ForeignKey(
        "Question",
        on_delete=models.CASCADE,
        related_name="question_states",
    )


class Attempt(models.Model):
    module_name = models.CharField(max_length=255)
