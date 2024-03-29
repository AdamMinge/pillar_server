import datetime

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _
from rest_framework.settings import APISettings as _APISettings

USER_SETTINGS = getattr(settings, "AUTHENTICATION_APP", None)

DEFAULTS = {
    "EMAIL_SENDER": settings.EMAIL_HOST_USER,
    "EMAIL_LOGO": None,
    "EMAIL_SIGNATURE": None,
    "EMAIL_ACCOUNT_VERIFICATION_SUBJECT": "Verify your account {{ username }}",
    "EMAIL_ACCOUNT_VERIFICATION_PLAIN": "account_verification.txt",
    "EMAIL_ACCOUNT_VERIFICATION_HTML": "account_verification.html",
    "EMAIL_PASSWORD_RECOVERY_SUBJECT": "Recovery your password {{ username }}",
    "EMAIL_PASSWORD_RECOVERY_PLAIN": "password_recovery.txt",
    "EMAIL_PASSWORD_RECOVERY_HTML": "password_recovery.html",
    "TOKEN_GENERATOR_ALGORITHM": "HS256",
    "TOKEN_GENERATOR_SECRET": settings.SECRET_KEY,
    "ACCOUNT_VERIFICATION_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "PASSWORD_RECOVERY_TOKEN_LIFETIME": datetime.timedelta(minutes=15),
}

IMPORT_STRINGS = ()

REMOVED_SETTINGS = ()


class APISettings(_APISettings):
    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(f"The '{setting}' setting has been removed.")

        return user_settings


api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    global api_settings

    setting, value = kwargs["setting"], kwargs["value"]

    if setting == "AUTHENTICATION_APP":
        api_settings = APISettings(value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_api_settings)
