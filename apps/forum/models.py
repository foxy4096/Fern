from django.db import models
from apps.account.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(verbose_name=_("Description"),
        max_length=500,
        blank=True,
        help_text=_("Markdown and BBCode Supported"),)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    STATUS = (
        ("Draft", "Draft"),
        ("Published", "Published")
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=STATUS,
        default="Draft",
    )
    categories = models.ManyToManyField(
        verbose_name=_("Categories"),
        to=Category,
        related_name="posts",
        blank=True,
        help_text=_("Select categories for this post."),
    )
    author = models.ForeignKey(
        verbose_name=_("Author"),
        to=User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    likes = models.ManyToManyField(
        verbose_name=_("Likes"),
        to=User,
        blank=True,
        related_name="likes",
    )
    reply_to = models.ForeignKey(
        verbose_name=_("Reply To"),
        to="self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
    )

    def __str__(self):
        return self.title

    @property
    def get_likes_count(self):
        return self.likes.count()

    @property
    def get_replies_count(self):
        return self.replies.count()

    class Meta:
        ordering = ["-created_at"]
