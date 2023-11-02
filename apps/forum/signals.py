from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .utils import find_mentioned_users
from apps.notification.models import Notification


@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, **kwargs):
    if created:
        mentioned_users = find_mentioned_users(instance.body).exclude(
            username=instance.author.username
        )

        # Exclude the author (sender) from mentioned users
        mentioned_users = [user for user in mentioned_users if user != instance.author]

        # Create a notification for each mentioned user
        for user in mentioned_users:
            # Create a new mention notification
            Notification.objects.create(
                sender=instance.author,
                receiver=user,
                verb=f"{instance.author.username} mentioned you in a post.",
                content_object=instance,
            )


@receiver(post_save, sender=Post)
def reply_save_handler(sender, instance, created, **kwargs):
    if created and instance.parent.author != instance.author:
        # Create a reply notification
        Notification.objects.create(
            sender=instance.author,
            receiver=instance.parent.author,  # Assuming Reply has a reference to the parent post
            verb=f"{instance.author.username} replied to your post.",
            content_object=instance,
        )
