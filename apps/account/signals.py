from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.account.models import UserPreference, UserProfile, User
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)
        logger.info(f"Created profile for {instance.username}")

