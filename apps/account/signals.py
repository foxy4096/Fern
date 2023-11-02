from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import UserPreference, UserProfile, User, get_sentinel_user
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver to create user profile and preferences when a new user is created.

    Args:
        sender: The sender of the signal.
        instance: The User instance being saved.
        created: A boolean indicating if the user was just created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)
        logger.info(f"Created profile for {instance.username}")


@receiver(post_migrate)
def create_ghost_user(sender, **kwargs):
    """
    Signal receiver to create a ghost user to represent the deleted user.

    Args:
        sender: The sender of the signal.
        **kwargs: Additional keyword arguments.
    """
    get_sentinel_user()