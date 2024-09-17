# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/speech1/', consumers.SpeechConsumer.as_asgi()),
]

