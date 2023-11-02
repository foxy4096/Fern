from django.db import models
from apps.account.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        verbose_name=_("Description"),
        max_length=500,
        blank=True,
        help_text=_("Markdown and BBCode Supported"),
    )

    def __str__(self):
        return self.name

    def get_recent_3_threads(self):
        return self.threads.order_by("-created_at")[:3]

    class Meta:
        verbose_name_plural = "Categories"


class Thread(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        verbose_name=_("Category"),
        to=Category,
        related_name="threads",
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        help_text=_("Select category for this post."),
    )
    creator = models.ForeignKey(
        verbose_name=_("Author"),
        to=User,
        on_delete=models.CASCADE,
        related_name="threads",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    is_locked = models.bool = models.BooleanField(
        verbose_name=_("Locked"),
        help_text=_("Locked threads cannot be replied to."),
        default=False,
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    STATUS = (("Draft", "Draft"), ("Published", "Published"))
    thread = models.ForeignKey(
        verbose_name=_("Thread"),
        to=Thread,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=10,
        choices=STATUS,
        default="Published",
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
    parent = models.ForeignKey(
        verbose_name=_("Parent"),
        to="self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )

    def __str__(self):
        return f"{slugify(self.thread.title)}#{self.pk:04d}"

    def get_absolute_url(self):
        return reverse(
            "forum:post_detail",
            kwargs={"thread_pk": self.thread.pk, "post_pk": self.pk},
        )

    @property
    def get_likes_count(self):
        return self.likes.count()

    @property
    def get_replies_count(self):
        return self.replies.count()

    def get_replies(self):
        """
        Recursively get all replies of a post.
        """
        replies = self.children.all()
        for reply in replies:
            replies = replies | reply.get_replies()
        return replies

    class Meta:
        ordering = ["created_at"]
