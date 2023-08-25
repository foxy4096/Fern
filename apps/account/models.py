from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.contrib.sessions.models import Session

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name=_("User"), to=User, on_delete=models.CASCADE
    )
    bio = models.TextField(
        verbose_name=_("About Me"),
        max_length=500,
        blank=True,
        help_text=_("Tell us about yourself. (Markdown and BBCode Supported)"),
    )
    avatar = ResizedImageField(
        verbose_name=_("Profile Picture"),
        default="default/avatar.png",
        upload_to="avatars",
        size=[600, 600],
        crop=["middle", "center"],
    )
    muted_users = models.ManyToManyField(
        verbose_name=_("Muted Users"),
        to=User,
        related_name="muted_users",
    )

    def __str__(self):
        return self.user.get_username()


class UserPreference(models.Model):
    user = models.OneToOneField(
        verbose_name=_("user"), to=User, on_delete=models.CASCADE
    )
    email_notifications = models.BooleanField(default=True)
    email_notifications_frequency = models.CharField(
        verbose_name=_("Email Notifications Frequency"),
        max_length=20,
        choices=[
            ("Daily", "Daily"),
            ("Weekly", "Weekly"),
            ("Monthly", "Monthly"),
        ],
        default="Daily",
        help_text=_("How often do you want to receive email notifications?"),
    )

    def __str__(self):
        return f"{self.user.get_username()}'s Preference"


class UserSession(models.Model):
    session = models.OneToOneField(
        verbose_name=_("Session"), to=Session, on_delete=models.CASCADE
    )
    user = models.ForeignKey(verbose_name=_("User"), to=User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(verbose_name=_("IP Address"))
    user_agent = models.CharField(verbose_name=_("User Agent"), max_length=255)
    

    def __str__(self):
        return self.user.get_username()
