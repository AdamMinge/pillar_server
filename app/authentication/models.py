import uuid

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from rest_framework_api_key.models import AbstractAPIKey


class Organization(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=128,
        help_text=_(
            "The name of the organization. This field must "
            "be unique and should be kept short and memorable."
        ),
    )

    active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Whether the organization is currently active. "
            "This can be used to disable organizations without deleting them."
        ),
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")


class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        to=Organization,
        verbose_name=_("organization"),
        related_name="api_keys",
        on_delete=models.CASCADE,
        help_text=_(
            "The organization that the API key belongs to. "
            "This field is a foreign key to the Organization model."
        ),
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = _("Organization API key")
        verbose_name_plural = _("Organization API keys")


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have a Email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        verbose_name=_("id"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_(
            "A unique identifier for the user. This field is automatically "
            "generated and cannot be edited."
        ),
    )

    username = models.CharField(
        verbose_name=_("username"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_(
            "The user's username. This field must be unique and "
            "should be kept short and memorable."
        ),
    )

    email = models.EmailField(
        verbose_name=_("email"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_(
            "The user's email address. This field must "
            "be unique and is used for login."
        ),
    )

    is_verified = models.BooleanField(
        verbose_name=_("verified"),
        default=False,
        help_text=_(
            "Whether the user's email address has been verified. "
            "This can be used for email confirmation and account activation workflows."
        ),
    )

    is_active = models.BooleanField(
        verbose_name=_("activated"),
        default=True,
        help_text=_(
            "Whether the user's account is currently active. "
            "This can be used to disable user accounts without deleting them."
        ),
    )

    is_staff = models.BooleanField(
        verbose_name=_("staff"),
        default=False,
        help_text=_(
            "Whether the user is a member of staff. This can "
            "be used to give special permissions to certain users."
        ),
    )

    created_at = models.DateTimeField(
        verbose_name=_("created"),
        auto_now_add=True,
        help_text=_("he date and time when the user account was created."),
    )

    updated_at = models.DateTimeField(
        verbose_name=_("updated"),
        auto_now=True,
        help_text=_("The date and time when the user account was last updated."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        return str(self.email)
