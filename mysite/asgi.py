"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# from audio_processor.routing import websocket_urlpatterns as audio_processor_websocket_urlpatterns
# from speech_recognitions.routing import websocket_urlpatterns as speech_recognition_websocket_urlpatterns
# from STT.routing import websocket_urlpatterns as stt_websocket_urlpatterns
# ... existing imports ...

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

django_asgi_app = get_asgi_application()

async def debug_application(scope, receive, send):
    print(f"Debug ASGI: {scope['type']} - {scope['path']}", file=sys.stderr)
    sys.stderr.flush()
    return await django_asgi_app(scope, receive, send)

application = ProtocolTypeRouter({
    "http": debug_application,
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(
    #         stt_websocket_urlpatterns
    #     )
    # ),
})

# ... existing print statement ...
print("ASGI application initialized", file=sys.stderr)
sys.stderr.flush()