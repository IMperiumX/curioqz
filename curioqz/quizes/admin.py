from django.contrib import admin

from .models import Attempt, Grade, Quiz, QuizGrade, QuizQuestion, Review


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "topic",
        "introformat",
        "created",
        "modified",
        "time_open",
        "time_close",
        "time_limit",
        # "intro",
        "grade_method",
        "decimal_points",
        "question_per_page",
        "difficulty",
        "score_to_pass",
        "delay1",
        "delay2",
        "show_user_picture",
        "show_blocks",
        "shuffle_questions",
        "shuffle_answers",
        "course",
        "review",
    )
    list_filter = (
        "created",
        "modified",
        "time_open",
        "time_close",
        "show_user_picture",
        "show_blocks",
        "shuffle_questions",
        "shuffle_answers",
        "course",
        "review",
    )
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "marks",
        "right_answer",
        "correctness",
        "specific_feedback",
        "general_feedback",
        "overall_feedback",
        "reviewer",
    )
    list_filter = ("reviewer",)


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "start",
        "finish",
        "modified",
        "preview",
        "quiz",
        "user",
    )
    list_filter = ("start", "finish", "modified", "quiz", "user")
    search_fields = ("slug",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("id", "grade")


@admin.register(QuizGrade)
class QuizGradeAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "user", "grade", "modified")
    list_filter = ("quiz", "user", "grade", "modified")


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "questions")
    list_filter = ("quiz", "questions")
