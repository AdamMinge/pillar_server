from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from authentication.utils import (
    EmailVerificationTokenGenerator,
    EmailVerificationTokenSender,
)


_token_generator = EmailVerificationTokenGenerator()
_token_sender = EmailVerificationTokenSender()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        max_length=getattr(settings, "MAX_PASSWORD_LENGTH", 60),
        min_length=getattr(settings, "MIN_PASSWORD_LENGTH", 10),
        write_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = [
            "url",
            "username",
            "password",
            "email",
            "verified",
            "activated",
            "staff",
            "created",
            "updated",
        ]
        read_only_fields = [
            "url",
            "verified",
            "activated",
            "staff",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "url": {"view_name": "user-detail", "lookup_field": "id"},
            "verified": {"source": "is_verified"},
            "activated": {"source": "is_active"},
            "staff": {"source": "is_staff"},
            "created": {"source": "created_at"},
            "updated": {"source": "updated_at"},
        }

    def save(self, **kwargs):
        user = super().save(**kwargs)
        assert user is not None

        token, _ = _token_generator.make_token(user)
        _token_sender.send(user, token)

        return user


class SendActivationEmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3, write_only=True)

    default_error_messages = {
        "invalid_email": _("Email used to obtain verification token is not valid"),
        "verified_email": _(
            "Email used to obtain verification token is already verified"
        ),
    }

    def validate_email(self, email):
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            self.fail("invalid_email")

        if user.is_verified:
            self.fail("verified_email")

        assert user is not None
        token, _ = _token_generator.make_token(user)
        _token_sender.send(user, token)

        return email

    def create(self, validated_data):
        raise NotImplementedError


class VerifyActivationEmailTokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    default_error_messages = {
        "invalid_token": _("Token used to email verification is not valid"),
        "verified_email": _(
            "Email used to obtain verification token is already verified"
        ),
    }

    def validate_token(self, token):
        valid, user = _token_generator.check_token(token)
        if not valid:
            self.fail("invalid_token")
        if user.is_verified:
            self.fail("verified_email")

        assert user is not None
        user.is_verified = True
        user.save()

        return token

    def create(self, validated_data):
        raise NotImplementedError
