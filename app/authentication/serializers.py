from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, ValidationError
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from authentication.utils import (
    AccountVerificationTokenGenerator,
    PasswordRecoveryTokenGenerator,
    AccountVerificationSender,
    PasswordRecoverySender,
)


_account_verification_token_generator = AccountVerificationTokenGenerator()
_password_recovery_token_generator = PasswordRecoveryTokenGenerator()

_account_verification_sender = AccountVerificationSender()
_password_recovery_sender = PasswordRecoverySender()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

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

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        assert password is not None

        user = super().create(validated_data)
        assert user is not None

        user.set_password(password)
        user.save()

        token, _ = _account_verification_token_generator.make_token(user)
        _account_verification_sender.send(user, token)

        return user


class SendActivationEmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3, write_only=True)
    url = serializers.URLField(write_only=True)

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

        return email

    def save(self):
        email = self.validated_data["email"]
        url = self.validated_data["url"]

        user = get_user_model().objects.get(email=email)
        token, _ = _account_verification_token_generator.make_token(user)

        _account_verification_sender.send(user, url, token)


class SendRecoveryPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=3, write_only=True)
    url = serializers.URLField(write_only=True)

    default_error_messages = {
        "invalid_email": _("Email used to obtain password recovery token is not valid"),
    }

    def validate_email(self, email):
        if not get_user_model().objects.filter(email=email).exists():
            self.fail("invalid_email")
        return email

    def save(self):
        email = self.validated_data["email"]
        url = self.validated_data["url"]

        user = get_user_model().objects.get(email=email)
        token, _ = _password_recovery_token_generator.make_token(user)

        _password_recovery_sender.send(user, url, token)


class VerifyActivationEmailTokenSerializer(serializers.Serializer):
    default_error_messages = {
        "invalid_token": _("Token used to email verification is not valid"),
        "missing_token": _("Token used to email verification is missing"),
        "verified_email": _(
            "Email used to obtain verification token is already verified"
        ),
    }

    def validate(self, attrs):
        token = self.context["token"]
        if not token:
            self.fail("missing_token")

        valid, user = _account_verification_token_generator.check_token(token)
        if not valid:
            self.fail("invalid_token")
        if user.is_verified:
            self.fail("verified_email")

        attrs["user"] = user

        return attrs

    def save(self):
        user = self.validated_data["user"]
        assert user is not None

        user.is_verified = True
        user.save()


class VerifyPasswordRecoveryTokenSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        "invalid_token": _("Token used to password recovery is not valid"),
        "missing_token": _("Token used to password recovery is missing"),
    }

    def validate(self, attrs):
        token = self.context["token"]
        if not token:
            self.fail("missing_token")

        valid, user = _password_recovery_token_generator.check_token(token)
        if not valid:
            self.fail("invalid_token")

        attrs["user"] = user

        return attrs

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def save(self):
        user = self.validated_data["user"]
        password = self.validated_data["password"]

        assert user is not None
        assert user is not None

        user.set_password(password)
        user.save()
