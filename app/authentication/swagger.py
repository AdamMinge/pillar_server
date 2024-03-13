from django.utils.translation import ugettext as _

from rest_framework import status, serializers

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from authentication.serializers import UserSerializer


# =====================================================
#                   Swagger Serializers
# =====================================================


class TokenObtainPairResponseSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    access = serializers.CharField()


# =====================================================
#                   Swagger Decorators
# =====================================================

extend_obtain_token_pair_schema = extend_schema_view(
    post=extend_schema(
        description=_("Obtain Token Pair"),
        responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer},
    )
)

extend_refresh_token_schema = extend_schema_view(
    post=extend_schema(
        description=_("Refresh Token"),
        responses={status.HTTP_200_OK: TokenRefreshResponseSerializer},
    )
)

extend_verify_token_schema = extend_schema_view(
    post=extend_schema(
        description=_("Verify Token"), responses={status.HTTP_200_OK: OpenApiResponse()}
    )
)

extend_blacklist_token_schema = extend_schema_view(
    post=extend_schema(
        description=_("Blacklist Token"),
        responses={status.HTTP_200_OK: OpenApiResponse()},
    )
)

extend_signup_schema = extend_schema_view(
    post=extend_schema(
        description=_("Signup"), responses={status.HTTP_201_CREATED: UserSerializer}
    )
)

extend_verify_activation_email_token_schema = extend_schema_view(
    post=extend_schema(
        description=_("Verify Activation Email Token"),
        responses={status.HTTP_200_OK: OpenApiResponse()},
    )
)

extend_send_activation_email_token_schema = extend_schema_view(
    post=extend_schema(
        description=_("Send Activation Email Token"),
        responses={status.HTTP_200_OK: OpenApiResponse()},
    )
)

extend_user_list_schema = extend_schema_view(
    get=extend_schema(
        description=_("Obtain Users"), responses={status.HTTP_200_OK: UserSerializer}
    )
)

extend_user_detail_schema = extend_schema_view(
    get=extend_schema(
        description=_("Obtain User"), responses={status.HTTP_200_OK: UserSerializer}
    )
)
