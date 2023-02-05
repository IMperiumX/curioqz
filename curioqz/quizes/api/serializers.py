from django.contrib.auth import get_user_model
from rest_framework import serializers

from curioqz.courses.api.serializers import CourseSerializer
from curioqz.quizes.models import Attempt, Grade, Quiz, QuizGrade, QuizQuestion, Review

User = get_user_model()


class QuizSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Quiz
        fields = "__all__"


class QuizGradeSerializer(serializers.Serializer):
    url = serializers.CharField(source="grade.grade", read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = QuizGrade
        fields = ["url", "user"]


class QuizQuestionSerializer:
    ...


class ReviewSerializer:
    ...


class AttemptSerializer:
    ...


class GradeSerializer:
    ...
