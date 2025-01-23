from dj_rest_auth.registration.views import SocialAccountDisconnectView
from dj_rest_auth.registration.views import SocialAccountListView
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from quizify.authentication.api.views import TokenCreateAPIView
from quizify.users.api.views import FacebookLogin
from quizify.users.api.views import GitHubLogin
from quizify.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls


urlpatterns += [
    path("auth/", TokenCreateAPIView.as_view(), name="user-auth"),
    path("tokens/", TokenCreateAPIView.as_view(), name="auth-token"),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("github/", GitHubLogin.as_view(), name="github_login"),
]


urlpatterns += [
    path(
        "socialaccounts/",
        SocialAccountListView.as_view(),
        name="social_account_list",
    ),
    path(
        "socialaccounts/<int:pk>/disconnect/",
        SocialAccountDisconnectView.as_view(),
        name="social_account_disconnect",
    ),
]
