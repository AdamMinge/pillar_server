from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(user_id):
    # pylint: disable=import-outside-toplevel
    from django.contrib.auth.models import AnonymousUser

    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # pylint: disable=import-outside-toplevel
        from rest_framework_simplejwt.tokens import AccessToken, TokenError
        from django.contrib.auth.models import AnonymousUser

        try:
            token = dict(scope["headers"])["sec-websocket-protocol"].decode("utf-8")
        except ValueError:
            token = None

        try:
            access_token = AccessToken(token)
            scope["user"] = await get_user(access_token["user_id"])
        except TokenError:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
