from django.urls import path

from authentication.views import (
    ObtainTokenPairView,
    RefreshTokenView,
    VerifyTokenView,
    BlacklistTokenView,
    SignupView,
    VerifyActivationEmailTokenView,
    VerifyPasswordRecoveryTokenView,
    SendActivationEmailTokenView,
    SendPasswordRecoveryTokenView,
    UserList,
    UserDetail,
)

urlpatterns = [
    path("auth/login/", ObtainTokenPairView.as_view(), name="login"),
    path("auth/refresh/", RefreshTokenView.as_view(), name="login-refresh"),
    path("auth/verify/", VerifyTokenView.as_view(), name="login-verify"),
    path("auth/blacklist/", BlacklistTokenView.as_view(), name="login-blacklist"),
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path(
        "auth/recovery/<str:token>/",
        VerifyPasswordRecoveryTokenView.as_view(),
        name="auth-recovery",
    ),
    path(
        "auth/activation/<str:token>/",
        VerifyActivationEmailTokenView.as_view(),
        name="auth-activation",
    ),
    path(
        "auth/send_recovery/",
        SendPasswordRecoveryTokenView.as_view(),
        name="auth-send_recovery",
    ),
    path(
        "auth/send_activation/",
        SendActivationEmailTokenView.as_view(),
        name="auth-send-activation",
    ),
    path("user/", UserList.as_view(), name="user-list"),
    path("user/<uuid:id>/", UserDetail.as_view(), name="user-detail"),
]
