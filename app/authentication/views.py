from django.contrib.auth import get_user_model

from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from base.views import AccessPolicyViewSetMixin

from authentication.filters import UserFilter
from authentication.policies import OrganizationAPIKeyAccessPolicy, UserAccessPolicy
from authentication.serializers import (
    UserSerializer,
    SendActivationEmailTokenSerializer,
    VerifyActivationEmailTokenSerializer,
)
from authentication.swagger import (
    extend_obtain_token_pair_schema,
    extend_refresh_token_schema,
    extend_verify_token_schema,
    extend_blacklist_token_schema,
    extend_signup_schema,
    extend_verify_activation_email_token_schema,
    extend_send_activation_email_token_schema,
    extend_user_list_schema,
    extend_user_detail_schema,
)


@extend_obtain_token_pair_schema
class ObtainTokenPairView(AccessPolicyViewSetMixin, TokenObtainPairView):
    access_policy = OrganizationAPIKeyAccessPolicy


@extend_refresh_token_schema
class RefreshTokenView(AccessPolicyViewSetMixin, TokenRefreshView):
    access_policy = OrganizationAPIKeyAccessPolicy


@extend_verify_token_schema
class VerifyTokenView(AccessPolicyViewSetMixin, TokenVerifyView):
    access_policy = OrganizationAPIKeyAccessPolicy


@extend_blacklist_token_schema
class BlacklistTokenView(AccessPolicyViewSetMixin, TokenBlacklistView):
    access_policy = OrganizationAPIKeyAccessPolicy


@extend_signup_schema
class SignupView(AccessPolicyViewSetMixin, generics.CreateAPIView):
    serializer_class = UserSerializer
    access_policy = OrganizationAPIKeyAccessPolicy


@extend_verify_activation_email_token_schema
class VerifyActivationEmailTokenView(AccessPolicyViewSetMixin, generics.GenericAPIView):
    serializer_class = VerifyActivationEmailTokenSerializer
    access_policy = OrganizationAPIKeyAccessPolicy

    def post(self, request: Request, *_args, **_kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)


@extend_send_activation_email_token_schema
class SendActivationEmailTokenView(AccessPolicyViewSetMixin, generics.GenericAPIView):
    serializer_class = SendActivationEmailTokenSerializer
    access_policy = OrganizationAPIKeyAccessPolicy

    def post(self, request: Request, *_args, **_kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)


@extend_user_list_schema
class UserList(AccessPolicyViewSetMixin, generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    access_policy = UserAccessPolicy
    filterset_class = UserFilter
    lookup_field = "id"


@extend_user_detail_schema
class UserDetail(AccessPolicyViewSetMixin, generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    access_policy = UserAccessPolicy
    lookup_field = "id"
