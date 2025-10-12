from django.shortcuts import redirect, render, get_object_or_404, resolve_url
from apps.core.utils import paginate, is_hx_paginated, is_htmx
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from apps.notification.models import Notification
from django.contrib.contenttypes.models import ContentType

from .models import Post, Thread, Category, Upload


@login_required
def reply_form(request, pk):
    from .forms import ReplyCreationForm

    post = get_object_or_404(Post, pk=pk)
    form = ReplyCreationForm()
    return render(
        request, "forum/islands/reply_form.html", {"reply_form": form, "post": post}
    )


@login_required
def thread_post_list(request, pk):
    """
    Display the list of posts in a thread.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the thread to display.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    thread = get_object_or_404(Thread, pk=pk)
    posts = paginate(request, thread.posts.all())
    url = resolve_url("forum:thread_post_list", thread.pk)
    return render(request, "forum/islands/post_list.html", {"posts": posts, "url": url})


@login_required
def reply_button(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "forum/islands/reply_button.html", {"post": post})


@login_required
def post_block(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "forum/islands/post_block.html", {"post": post})


def insert_upload(request, pk):
    media = get_object_or_404(Upload, pk=pk)
    url = media.file.url
    filename = media.file.name.split("/")[-1]

    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        markdown = f"![{filename}]({url})"
    else:
        markdown = f"[{filename}]({url})"

    return HttpResponse(markdown, content_type="text/plain")


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        if post.author != request.user:
            post_ct = ContentType.objects.get_for_model(Post)

            Notification.objects.get_or_create(
                sender=request.user,
                receiver=post.author,
                verb=f"{request.user.username} liked your post.",
                content_type=post_ct,
                object_id=post.pk,
            )
    if is_htmx(request):
        return render(request, "forum/islands/like_button.html", {"post": post})
    else:
        return redirect(
            "forum:thread_detail", thread_slug=post.thread.slug
        )


@login_required
def upload_modal(request):
    """
    Renders the upload modal.
    """
    return render(request, "forum/islands/upload_modal.html")


@login_required
def upload_form(request):
    from .forms import UploadForm

    form = UploadForm()
    return render(request, "forum/islands/upload_form.html", {"form": form})


@login_required
def existing_uploads(request):
    uploads = Upload.objects.filter(user=request.user).order_by("-uploaded_at")
    total_used_bytes = sum(upload.file.size for upload in uploads if upload.file)
    total_used_mb = round(total_used_bytes / (1024 * 1024), 2)
    quota_mb = 50
    return render(
        request,
        "forum/islands/existing_uploads.html",
        {"uploads": uploads, "total_used_mb": total_used_mb, "quota_mb": quota_mb},
    )


def close_modal(request):
    return render(request, "forum/islands/empty.html")


def category_filter(request):
    """
    Renders the category filter UI, one level at a time.
    HTMX endpoint: loads next level of subcategories.
    """
    slug = request.GET.get("slug")
    category = get_object_or_404(Category, slug=slug) if slug else None
    subcategories = (
        category.subcategories.all()
        if category
        else Category.objects.filter(parent__isnull=True)
    )
    return render(
        request,
        "forum/islands/category_filter_form.html",
        {
            "category": category,
            "subcategories": subcategories,
        },
    )
