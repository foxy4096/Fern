from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from .utils import get_gravatar

User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username="ghost", is_active=False)[0]


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
    dark_mode = models.BooleanField(
        verbose_name=_("Dark Mode"),
        default=False,
        help_text=_("Enable dark mode for the website"),
    )
    avatar = ResizedImageField(
        verbose_name=_("Profile Picture"),
        default="default/avatar.png",
        upload_to="avatars",
        size=[600, 600],
        crop=["middle", "center"],
    )
    header = ResizedImageField(
        verbose_name=_("Header Picture"),
        upload_to="headers",
        size=[1600, 400],
        crop=["middle", "center"],
        blank=True,
        null=True,
    )
    use_gravtar = models.BooleanField(
        verbose_name=_("Use Gravatar"),
        default=False,
        help_text=_("Use Gravatar instead of a profile picture"),
    )
    muted_users = models.ManyToManyField(
        verbose_name=_("Muted Users"),
        to=User,
        related_name="muted_users",
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=30,
        blank=True,
        help_text=_("City, State, Country"),
    )
    website = models.URLField(
        verbose_name=_("Website"),
        max_length=100,
        blank=True,
        help_text=_("Your Website URL"),
    )

    rank = models.IntegerField(
        default=0,
        verbose_name=_("Rank"),
        help_text=_("The rank of the user in the leaderboard"),
    )

    def __str__(self):
        return self.user.get_username()

    def avatar_image(self):
        """
        Returns the avatar image url or Gravatar image url
        """
        return get_gravatar(self.user.email) if self.use_gravtar else self.avatar.url


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
