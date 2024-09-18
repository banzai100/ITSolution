from django.urls import path
from .views import video_view

urlpatterns = [
    path('runtext', video_view, name='video'),
]