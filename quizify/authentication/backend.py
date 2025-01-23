from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework import authentication
from rest_framework import exceptions

from quizify.common.utils.django import get_object_or_none


class TokenScheme(OpenApiAuthenticationExtension):
    target_class = "quizify.authentication.backend.AccessTokenAuthentication"
    name = "Access Token (redis)"
    match_subclasses = True
    priority = -1

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix=self.target.keyword,
        )


class AccessTokenAuthentication(authentication.BaseAuthentication):
    keyword = "Bearer"
    model = get_user_model()

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = _("Invalid token header. Sign string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Sign string should not contain invalid characters.",
            )
            raise exceptions.AuthenticationFailed(msg) from None
        user, header = self.authenticate_credentials(token)

        user.date_api_key_last_used = timezone.now()
        user.save(update_fields=["date_api_key_last_used"])
        return user, header

    @staticmethod
    def authenticate_credentials(token):
        model = get_user_model()
        user_id = cache.get(token)
        user = get_object_or_none(model, id=user_id)

        if not user:
            msg = _("Invalid token or cache refreshed.")
            raise exceptions.AuthenticationFailed(msg)
        return user, None

    def authenticate_header(self, request):
        return self.keyword
