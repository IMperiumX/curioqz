from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    name = "curioqz.questions"

    def ready(self):
        try:
            import curioqz.questions.signals  # noqa F401
        except ImportError:
            pass
