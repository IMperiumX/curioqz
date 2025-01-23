from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException

from quizify.users.utils import LoginBlockUtil
from quizify.users.utils import LoginIpBlockUtil

from .signals import post_auth_failed

reason_user_not_exist = "user_not_exist"
reason_password_failed = "password_failed"  # noqa: S105
reason_user_inactive = "user_inactive"


reason_choices = {
    reason_password_failed: _("Username/password check failed"),
    reason_user_not_exist: _("Username does not exist"),
    reason_user_inactive: _("This account is inactive."),
}


block_ip_login_msg = _(
    "The address has been locked "
    "(please contact admin to unlock it or try again after {} minutes)"
)
invalid_login_msg = _(
    "The email or password you entered is incorrect, "
    "please enter it again. "
    "You can also try {times_try} times "
    "(The account will be temporarily locked for {block_time} minutes)"
)
block_user_login_msg = _(
    "The account has been locked "
    "(please contact admin to unlock it or try again after {} minutes)"
)


class AuthFailedError(Exception):
    email = ""
    msg = ""
    error = ""
    request = None
    ip = ""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def as_data(self):
        return {
            "error": self.error,
            "msg": self.msg,
        }

    def __str__(self):
        return str(self.msg)


class SessionEmptyError(AuthFailedError):
    msg = _("No session found, check your cookie")
    error = "session_empty"


class QuizifyException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class NeedRedirectError(QuizifyException):
    def __init__(self, url, *args, **kwargs):
        self.url = url


class PasswordTooSimpleError(NeedRedirectError):
    default_code = "passwd_too_simple"
    default_detail = _("Your password is too simple, please change it for security")

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)


class PasswordNeedUpdateError(NeedRedirectError):
    default_code = "passwd_need_update"
    default_detail = _("You should to change your password before login")

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)


class PasswordRequireResetError(NeedRedirectError):
    default_code = "passwd_has_expired"
    default_detail = _("Your password has expired, please reset before logging in")

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)


class AuthFailedNeedLogMixin:
    email = ""
    request = None
    error = ""
    msg = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        post_auth_failed.send(
            sender=self.__class__,
            email=self.email,
            request=self.request,
            reason=self.msg,
        )


class AuthFailedNeedBlockMixin:
    email = ""
    ip = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        LoginBlockUtil(self.email, self.ip).incr_failed_count()


class BlockGlobalIpLoginError(AuthFailedError):
    error = "block_global_ip_login"

    def __init__(self, email, ip, **kwargs):
        if not self.msg:
            self.msg = block_ip_login_msg.format(
                settings.SECURITY_LOGIN_IP_LIMIT_TIME,
            )
        LoginIpBlockUtil(ip).set_block_if_need()
        super().__init__(email=email, ip=ip, **kwargs)


class CredentialError(
    AuthFailedNeedLogMixin,
    AuthFailedNeedBlockMixin,
    BlockGlobalIpLoginError,
    AuthFailedError,
):
    def __init__(self, error, email, ip, request):
        util = LoginBlockUtil(email, ip)
        times_remainder = util.get_remainder_times()
        block_time = settings.SECURITY_LOGIN_LIMIT_TIME
        if times_remainder < 1:
            self.msg = block_user_login_msg.format(settings.SECURITY_LOGIN_LIMIT_TIME)
        else:
            default_msg = invalid_login_msg.format(
                times_try=times_remainder,
                block_time=block_time,
            )
            if error == reason_password_failed:
                self.msg = default_msg
            else:
                self.msg = reason_choices.get(error, default_msg)
        # 先处理 msg 在 super，记录日志时原因才准确
        super().__init__(error=error, email=email, ip=ip, request=request)
