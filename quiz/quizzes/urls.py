from django.urls import path

from .views import QuizListView, quiz_data_view, quiz_view, save_quiz_view

app_name = "quizzes"

urlpatterns = [
    path("", QuizListView.as_view(), name="main-view"),
    path("<pk>/", quiz_view, name="quiz-view"),
    path("<pk>/save/", save_quiz_view, name="save-view"),
    path("<pk>/data/", quiz_data_view, name="quiz-data-view"),
]
