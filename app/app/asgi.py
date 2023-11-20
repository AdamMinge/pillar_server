import os

from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from authentication.middleware import TokenAuthMiddleware
from authentication import routing as auth_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

django_asgi_api = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_api,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(
                    [
                        *auth_routing.websocket_urlpatterns,
                    ]
                )
            ),
        ),
    }
)
