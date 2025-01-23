import datetime
import logging
from collections.abc import Callable
from functools import partial

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request

from quizify.common.utils import bulk_get
from quizify.common.utils import get_request_ip
from quizify.users.signals import post_user_change_password
from quizify.users.utils import LoginBlockUtil
from quizify.users.utils import LoginIpBlockUtil

from . import errors
from .signals import post_auth_failed
from .signals import post_auth_success

logger = logging.getLogger(__name__)


class CommonMixin:
    request: Request
    _ip = ""

    def raise_credential_error(self, error):
        raise self.partial_credential_error(error=error)

    def get_request_ip(self):
        if not self._ip:
            self._ip = get_request_ip(self.request)
        return self._ip

    def _set_partial_credential_error(self, email, ip, request):
        self.partial_credential_error = partial(
            errors.CredentialError,
            email=email,
            ip=ip,
            request=request,
        )

    def get_auth_data(self, data):
        request = self.request

        items = ["email", "password"]
        (
            email,
            password,
        ) = bulk_get(
            data,
            items,
            default="",
        )
        ip = self.get_request_ip()
        self._set_partial_credential_error(email=email, ip=ip, request=request)
        return email, password, ip


class AuthPreCheckMixin:
    request: Request
    get_request_ip: Callable
    raise_credential_error: Callable

    def _check_is_block(self, email):
        ip = self.get_request_ip()

        if LoginIpBlockUtil(ip).is_block():
            raise errors.BlockGlobalIpLoginError(email=email, ip=ip)

        is_block = LoginBlockUtil(email, ip).is_block()
        if not is_block:
            return False
        msg = f"IP was blocked: {email}:{ip}"
        logger.warning(msg)
        raise errors.BlockLoginError(email=email, ip=ip)

    def check_is_block(self):
        if hasattr(self.request, "data"):
            email = self.request.data.get("email")
        else:
            email = self.request.POST.get("email")

        self._check_is_block(email)

    def _check_only_allow_exists_user_auth(self, email):
        from quizify.users.models import User

        # Only allow pre-existing user authentication
        if not settings.ONLY_ALLOW_EXIST_USER_AUTH:
            return

        exist = User.objects.filter(email=email).exists()
        if not exist:
            msg = f"Only allow exist user auth, login failed: {email}"
            logger.error(msg)
            self.raise_credential_error(errors.reason_user_not_exist)


class AuthPostCheckMixin:
    @classmethod
    def _check_passwd_is_too_simple(cls, user, password):
        if user.check_passwd_too_simple(password):
            message = _("Your password is too simple, please change it for security")
            url = cls.generate_reset_password_url_with_flash_msg(user, message=message)
            raise errors.PasswordTooSimple(url)

    @classmethod
    def _check_passwd_need_update(cls, user):
        if user.check_need_update_password():
            message = _("You should to change your password before login")
            url = cls.generate_reset_password_url_with_flash_msg(user, message)
            raise errors.PasswordNeedUpdate(url)

    @classmethod
    def _check_password_require_reset_or_not(cls, user):
        if user.password_has_expired:
            message = _("Your password has expired, please reset before logging in")
            url = cls.generate_reset_password_url_with_flash_msg(user, message)
            raise errors.PasswordRequireResetError(url)


class AuthMixin(CommonMixin, AuthPreCheckMixin, AuthPostCheckMixin):
    date_password_last_updated: datetime.datetime
    sect_cache_tpl = "user_sect_{}"
    need_update_password: bool
    id: str

    def set_password(self, raw_password):
        if self.can_update_password():
            if self.email:
                self.date_password_last_updated = timezone.now()
                post_user_change_password.send(self.__class__, user=self)
            super().set_password(raw_password)

    def check_user_auth(self, valid_data=None):
        # pre check
        self.check_is_block()
        email, password, ip = self.get_auth_data(valid_data)
        self._check_only_allow_exists_user_auth(email)

        # check auth
        user = authenticate(self.request, **valid_data)

        if not user:
            self.raise_credential_error(errors.reason_password_failed)

        elif not user.is_active:
            self.raise_credential_error(errors.reason_user_inactive)

        # TODO: Create => Verify login-acl rules

        # post check
        self._check_password_require_reset_or_not(user)
        self._check_passwd_is_too_simple(user, password)
        self._check_passwd_need_update(user)
        user.cache_login_password_if_need(password)

        LoginBlockUtil(user.email, ip).clean_failed_count()
        LoginIpBlockUtil(ip).clean_block_if_need()
        return user

    @staticmethod
    def check_passwd_too_simple(password):
        simple_passwords = ["admin", "ChangeMe"]
        return password in simple_passwords

    def send_success_auth_signal(self, user):
        post_auth_success.send(
            sender=self.__class__,
            user=user,
            request=self.request,
        )

    def send_failed_auth_signal(self, email="", reason=""):
        post_auth_failed.send(
            sender=self.__class__,
            email=email,
            request=self.request,
            reason=reason,
        )

    def cache_login_password_if_need(self, password):
        from quizify.common.utils import signer

        if not settings.CACHE_LOGIN_PASSWORD_ENABLED:
            return
        if not password:
            return
        key = self.sect_cache_tpl.format(self.id)
        ttl = settings.CACHE_LOGIN_PASSWORD_TTL
        if not isinstance(ttl, int) or ttl <= 0:
            return
        secret = signer.sign(password)
        cache.set(key, secret, ttl)

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.need_update_password = False
        self.save()

    def check_need_update_password(self):
        return self.need_update_password

    @property
    def date_password_expired(self):
        interval = settings.SECURITY_PASSWORD_EXPIRATION_TIME
        return self.date_password_last_updated + timezone.timedelta(days=int(interval))

    @property
    def password_expired_remain_days(self):
        date_remain = self.date_password_expired - timezone.now()
        return date_remain.days

    @property
    def password_has_expired(self):
        return self.password_expired_remain_days < 0
