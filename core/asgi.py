"""
ASGI config for booking project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from websocketing.consumers import ReportConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

asgi_app = get_asgi_application()

urlpatterns = [
    path('ws/<str:report_id>', ReportConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'http': asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(urlpatterns))
})
