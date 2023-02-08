from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from curioqz.questions.api.serializers import QuestionSerializer
from curioqz.questions.models import Question


class QuestionViewSet(GenericViewSet, ListModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
