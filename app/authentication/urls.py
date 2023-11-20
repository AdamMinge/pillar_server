from django.urls import path

from authentication.views import (
    ObtainTokenPairView,
    RefreshTokenView,
    VerifyTokenView,
    BlacklistTokenView,
    RegisterView,
    VerifyActivationEmailTokenView,
    SendActivationEmailTokenView,
    UserList,
    UserDetail,
)

urlpatterns = [
    path("auth/login/", ObtainTokenPairView.as_view(), name="login"),
    path("auth/login/refresh/", RefreshTokenView.as_view(), name="login-refresh"),
    path("auth/login/verify/", VerifyTokenView.as_view(), name="login-verify"),
    path("auth/login/blacklist/", BlacklistTokenView.as_view(), name="login-blacklist"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path(
        "auth/register/activation/",
        VerifyActivationEmailTokenView.as_view(),
        name="register-activation",
    ),
    path(
        "auth/register/resend_activation/",
        SendActivationEmailTokenView.as_view(),
        name="register-resend_activation",
    ),
    path("user/", UserList.as_view(), name="user-list"),
    path("user/<uuid:id>/", UserDetail.as_view(), name="user-detail"),
]
