"""
ASGI config for ChatRoom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from Room.routing import websocket_url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatRoom.settings')

application = get_asgi_application()

import Room.routing

channel_application = ProtocolTypeRouter({
    "http": application,
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_url))
    )
    # Just HTTP for now. (We can add other protocols later.)
})