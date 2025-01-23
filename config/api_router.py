from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from quizify.authentication.api.views import TokenCreateAPIView
from quizify.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls


urlpatterns += [
    path("auth/", TokenCreateAPIView.as_view(), name="user-auth"),
    path("tokens/", TokenCreateAPIView.as_view(), name="auth-token"),
]
