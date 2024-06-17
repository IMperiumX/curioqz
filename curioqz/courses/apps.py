from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoursesConfig(AppConfig):
    name = "curioqz.courses"
    verbose_name = _("Courses")

    def ready(self):
        try:
            import curioqz.courses.signals  # noqa F401
        except ImportError:
            pass
