from django.urls import path

from authentication.views import (
    ObtainTokenPairView,
    RefreshTokenView,
    VerifyTokenView,
    BlacklistTokenView,
    SignupView,
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
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path(
        "auth/signup/activation/",
        VerifyActivationEmailTokenView.as_view(),
        name="signup-activation",
    ),
    path(
        "auth/signup/resend_activation/",
        SendActivationEmailTokenView.as_view(),
        name="signup-resend_activation",
    ),
    path("user/", UserList.as_view(), name="user-list"),
    path("user/<uuid:id>/", UserDetail.as_view(), name="user-detail"),
]
