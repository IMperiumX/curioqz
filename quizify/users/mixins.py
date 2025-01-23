import base64

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from quizify.common.utils import random_string


class TokenMixin:
    email = ""
    id = None

    def create_bearer_token(self, request=None, age=None):
        expiration = age or settings.TOKEN_EXPIRATION or 3600
        remote_addr = request.META.get("REMOTE_ADDR", "") if request else "0.0.0.0"  # noqa: S104
        if not isinstance(remote_addr, bytes):
            remote_addr = remote_addr.encode("utf-8")
        remote_addr = base64.b16encode(remote_addr)  # .replace(b'=', '')
        cache_key = f"{self.id}_{remote_addr}"
        token = cache.get(cache_key)
        if not token:
            token = random_string(36)
        cache.set(token, self.id, expiration)
        cache.set(cache_key, token, expiration)
        date_expired = timezone.now() + timezone.timedelta(seconds=expiration)
        return token, date_expired

    def refresh_bearer_token(self, token):
        pass
