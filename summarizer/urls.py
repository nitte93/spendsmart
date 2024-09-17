from django.urls import path
from . import views

urlpatterns = [
    path('summarize/', views.summarize_youtube_video, name='summarize_youtube_video'),
]