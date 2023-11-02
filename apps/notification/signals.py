from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_group_{instance.receiver.username}",
        {"type": "send_notification", "message": instance},
    )
