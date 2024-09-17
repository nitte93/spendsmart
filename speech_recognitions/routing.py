from django.urls import re_path
from django.urls import include, path
from .consumers import SpeechRecognitionConsumer

websocket_urlpatterns = [
    path('ws/speech_recognition/', SpeechRecognitionConsumer.as_asgi()),
]