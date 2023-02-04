from rest_framework import mixins, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Course, Subject
from .permissions import IsEnrolled
from .serializers import (
    CourseSerializer,
    CourseWithContentsSerializer,
    SubjectSerializer,
)


class SubjectViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Course.objects.prefetch_related("modules__contents")
    serializer_class = CourseSerializer

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
