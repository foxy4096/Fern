from django.db import models
from apps.account.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
import os


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        verbose_name=_("Description"),
        max_length=500,
        blank=True,
        help_text=_("Markdown and BBCode Supported"),
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    color = ColorField(default="#007bff")
    parent = models.ForeignKey(
        verbose_name=_("Parent"),
        to="self",
        related_name="subcategories",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def get_recent_3_threads(self):
        return self.threads.order_by("-created_at")[:3]

    def get_absolute_url(self):
        return reverse("forum:threads_by_category", kwargs={"slug": self.slug})

    @property
    def is_leaf(self):
        """
        Check if the category is a leaf node (i.e., has no subcategories).
        """
        return not self.subcategories.exists()

    @property
    def is_root(self):
        """
        Check if the category is a root node (i.e., has no parent).
        """
        return self.parent is None

    def get_ancestors(self):
        """
        Get all ancestors of the category.
        Returns a list of categories from the root to this category.
        """
        ancestors = []
        current = self
        while current.parent:
            ancestors.append(current.parent)
            current = current.parent
        return ancestors[::-1]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        # Ensure the slug is unique
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Generate a unique slug for the category.
        """
        base_slug = slugify(self.name)
        unique_slug = base_slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        return unique_slug

    class Meta:
        verbose_name_plural = "Categories"


class Thread(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        verbose_name=_("Category"),
        to=Category,
        related_name="threads",
        on_delete=models.CASCADE,
        blank=True,
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

    is_locked = models.BooleanField(
        verbose_name=_("Locked"),
        help_text=_("Locked threads cannot be replied to."),
        default=False,
    )

    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def get_posts_count(self):
        """
        Get the count of posts in the thread.
        """
        return self.posts.count()

    @property
    def get_first_post(self):
        """
        Get the first post in the thread.
        """
        return self.posts.first()

    def get_absolute_url(self):
        return reverse("forum:thread_detail", kwargs={"slug": self.slug})


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
            kwargs={"thread_slug": self.thread.slug, "post_pk": self.pk},
        )

    @property
    def get_likes_count(self):
        return self.likes.count()

    @property
    def get_replies_count(self):
        return self.replies.count()

    def get_replies(self):
        """
        Iteratively get all replies of a post.
        """
        replies = list(self.children.all())
        all_replies = []
        while replies:
            reply = replies.pop(0)
            all_replies.append(reply)
            replies.extend(reply.children.all())
        return all_replies

    class Meta:
        ordering = ["created_at"]


class Link(models.Model):
    """
    Rich Reperesentation of a link.
    """

    title = models.CharField(max_length=255)
    url = models.URLField()
    clicks = models.IntegerField(default=0)
    post = models.ForeignKey(
        verbose_name=_("Post"),
        to=Post,
        related_name="links",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["clicks"]


class Upload(models.Model):
    file = models.FileField(upload_to="forum/uploads/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="forum_uploads", on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        max_file_size = 5 * 1024 * 1024  # 5 MB
        user_quota = 50 * 1024 * 1024  # 50 MB

        # ✅ Step 1: Ensure we actually have a file before accessing .size
        if not self.file or not hasattr(self.file, "size"):
            return  # Skip checks if no file is present (e.g., editing description)

        # ✅ Step 2: Check individual file size
        if self.file.size > max_file_size:
            raise ValidationError(_("Each file must be ≤ 5 MB."))

        # ✅ Step 3: Calculate total used space for the user (safe iteration)
        total_used = 0
        for upload in Upload.objects.filter(user=self.user).exclude(pk=self.pk):
            if upload.file and hasattr(upload.file, "size"):
                try:
                    total_used += upload.file.size
                except FileNotFoundError:
                    # In case a file was deleted manually from storage
                    continue

        # ✅ Step 4: Check quota
        if total_used + self.file.size > user_quota:
            remaining = max(0, user_quota - total_used)
            raise ValidationError(
                _(
                    f"Upload quota exceeded. You can only upload {remaining / (1024*1024):.2f} MB more."
                )
            )

    def __str__(self):
        return f"{self.file.name if self.file else 'No file'} ({self.user.username})"

    class Meta:
        ordering = ["-uploaded_at"]
