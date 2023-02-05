from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from curioqz.quizes.api.views import QuizGradeViewSet, QuizViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("quizes", QuizViewSet)
router.register("quiz-grades", QuizGradeViewSet)

app_name = "quizes"
urlpatterns = router.urls
