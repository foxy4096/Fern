from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserPreference, UserProfile, User, UserSession
from django.contrib.sessions.models import Session
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserPreference.objects.create(user=instance)
        logger.info(f"Created profile for {instance.username}")


# @receiver(post_save, sender=Session)
# def create_user_session(sender, instance, created, **kwargs):
#     if created:
#         user_id = instance.get_decoded().get("_auth_user_id")
#         UserSession.objects.create(session=instance, user_id=user_id)
#         logger.info(f"Created session for {instance.session_key}")
