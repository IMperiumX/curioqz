from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from quizify.authentication.mixins import AuthMixin

from .managers import UserManager
from .mixins import TokenMixin


class User(
    AuthMixin,
    TokenMixin,
    AbstractUser,
):
    """
    Default custom user model for quizify.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    date_password_last_updated = DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name=_("Date password last updated"),
    )
    need_update_password = BooleanField(
        default=False,
        verbose_name=_("Need update password"),
    )
    date_api_key_last_used = DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date api key used"),
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
