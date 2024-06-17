# Generated by Django 4.0.8 on 2023-02-05 12:45
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    """ """

    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("module_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Cagtegory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("info", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="QuestionAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fraction", models.DecimalField(decimal_places=0,
                                                 max_digits=3)),
                ("answer", models.TextField()),
                ("feedback", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="QuestionSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("newest", models.IntegerField(default=0)),
                ("new_graded", models.IntegerField(default=0)),
                ("sum_penalty",
                 models.DecimalField(decimal_places=0, max_digits=3)),
                ("comment", models.TextField()),
                ("flagged", models.BooleanField(default=False)),
                (
                    "attempt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="question_sessions",
                        to="questions.attempt",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer", models.TextField()),
                ("seq_number", models.IntegerField(default=0)),
                ("event", models.IntegerField(default=0)),
                ("grade", models.DecimalField(decimal_places=0, max_digits=3)),
                ("raw_grade",
                 models.DecimalField(decimal_places=0, max_digits=4)),
                ("penlity", models.DecimalField(decimal_places=0,
                                                max_digits=3)),
                (
                    "attempt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="question_states",
                        to="questions.attempt",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="question",
            name="default_grade",
            field=models.DecimalField(decimal_places=0,
                                      default=0,
                                      max_digits=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="question",
            name="general_feedback",
            field=models.TextField(default=" "),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="question",
            name="penalty",
            field=models.DecimalField(decimal_places=0,
                                      default=0,
                                      max_digits=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="answer",
            name="text",
            field=models.TextField(),
        ),
        migrations.DeleteModel(name="CorrectAnswer", ),
        migrations.AddField(
            model_name="state",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="question_states",
                to="questions.question",
            ),
        ),
        migrations.AddField(
            model_name="questionsession",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions_sessions",
                to="questions.question",
            ),
        ),
        migrations.AddField(
            model_name="questionanswer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="question_answers",
                to="questions.question",
            ),
        ),
    ]
