"""
ASGI config for django_settings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from final_course import urls

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_settings.settings")

asgi = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi,
        "websocket": AuthMiddlewareStack(URLRouter(urls.websocket_urlpatterns)),
    }
)
