from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuizesConfig(AppConfig):
    name = "curioqz.quizes"
    verbose_name = _("Quizes")

    def ready(self):
        try:
            import curioqz.quizes.signals  # noqa F401
        except ImportError:
            pass
