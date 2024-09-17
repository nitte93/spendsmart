from django.urls import re_path
from django.urls import include, path
from . import consumers

websocket_urlpatterns = [
    # path('ws/audio/', consumers.AudioProcessorConsumer.as_asgi()),
    # path('ws/test/', consumers.TestConsumer.as_asgi()),
    # re_path(r'', consumers.TestConsumer.as_asgi()),  # Catch-all route
]