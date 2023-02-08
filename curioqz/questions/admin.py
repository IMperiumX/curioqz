from django.contrib import admin

from .models import (
    Answer,
    Attempt,
    Cagtegory,
    Category,
    Question,
    QuestionAnswer,
    QuestionSession,
    State,
)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "text",
        "image",
        "type",
        "created",
        "hidden",
        "general_feedback",
        "default_grade",
        "penalty",
        "created_by",
        "category",
    )
    list_filter = ("created", "hidden", "created_by", "category")
    filter_horizontal = ("answers",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "created_by")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "info", "order")
    list_filter = ("created",)
    search_fields = ("name",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "correct", "created", "feedback")
    list_filter = ("correct", "created")
    search_fields = ("text",)


@admin.register(Cagtegory)
class CagtegoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "info", "created", "updated")
    list_filter = ("created", "updated")
    search_fields = ("name",)


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "fraction", "answer", "feedback", "question")
    list_filter = ("question",)


@admin.register(QuestionSession)
class QuestionSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "newest",
        "new_graded",
        "sum_penalty",
        "comment",
        "flagged",
        "attempt",
        "question",
    )
    list_filter = ("flagged", "attempt", "question")


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "answer",
        "seq_number",
        "event",
        "grade",
        "raw_grade",
        "penlity",
        "attempt",
        "question",
    )
    list_filter = ("attempt", "question")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "module_name")
