from django.urls import path
from . import consumers

urlpatterns = [
    path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),
]
