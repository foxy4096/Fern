from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from apps.notification.models import Notification


from apps.forum.forms import (
    PostCreationForm,
    ReplyCreationForm,
    ThreadCreationForm,
    CategoryFilterForm,
    UploadForm,
)
from apps.forum.models import Post, Thread, Category, Upload, Link
from .islands import thread_post_list
from apps.core.utils import paginate

from apps.core.utils import is_htmx
from django.conf import settings


@login_required
def thread_create(request, category_slug=None):
    """
    Create a new thread and handle form submissions.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response.
    """

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    else:
        category = None

    tform = ThreadCreationForm(
        request.POST if request.method == "POST" else None,
        initial={"category": category},
    )
    pform = PostCreationForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and tform.is_valid() and pform.is_valid():
        # Create a new thread
        thread = create_thread(request.user, tform)
        # Create the initial post in the thread
        create_initial_post(request.user, thread, pform)

        messages.success(request, "Your thread has been created!")
        return redirect("forum:thread_detail", slug=thread.slug)
    elif request.method == "POST":
        messages.error(request, "There was an error in your thread creation.")

    return render(request, "forum/thread_create.html", {"tform": tform, "pform": pform})


def create_thread(creator, tform):
    thread = tform.save(commit=False)
    thread.creator = creator
    thread.save()
    return thread


def create_initial_post(author, thread, pform):
    post = pform.save(commit=False)
    post.author = author
    post.thread = thread
    post.save()


def thread_detail(request, slug):
    thread = get_object_or_404(Thread, slug=slug)
    if is_htmx(request):
        return thread_post_list(request, thread.pk)
    posts = paginate(request, thread.posts.all())
    return render(
        request,
        "forum/thread_detail.html",
        {"thread": thread, "posts": posts},
    )


def post_detail(request, thread_slug, post_pk):
    """
    Display the details of a post and provide a form for creating replies.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to display.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    thread = get_object_or_404(Thread, slug=thread_slug)
    post = get_object_or_404(thread.posts.all(), pk=post_pk)
    return render(request, "forum/post_detail.html", {"post": post})


@login_required
def post_edit(request, pk):
    """
    Display a form for editing a post.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to edit.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostCreationForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been updated!")
            if is_htmx(request):
                return render(
                    request,
                    "forum/islands/post_block.html",
                    {"post": post},
                )
            return redirect("forum:thread_detail", slug=post.thread.slug)
        else:
            messages.error(request, "There was an error in your post update.")
    else:
        form = PostCreationForm(instance=post)
    if is_htmx(request):
        return render(
            request, "forum/islands/post_edit_form.html", {"form": form, "post": post}
        )
    return render(request, "forum/post_edit.html", {"form": form, "post": post})


@login_required
def reply_create(request, pk):
    """
    Create a new reply to a post and handle form submissions.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to reply to.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = ReplyCreationForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent = post
            reply.thread = post.thread
            reply.save()
            messages.success(request, "Your reply has been created!")
            return redirect("forum:thread_detail", slug=post.thread.slug)
        else:
            messages.error(request, "There was an error in your reply creation.")
    else:
        form = ReplyCreationForm()

    return render(
        request, "forum/reply_create.html", {"reply_form": form, "post": post}
    )


def threads_by_category(request, slug=""):
    category = get_object_or_404(Category, slug=slug)
    threads = Thread.objects.filter(category=category)
    threads = paginate(request, threads)
    category_filter_form = CategoryFilterForm(initial={"category": category})
    return render(
        request,
        "forum/threads_by_category.html",
        {
            "threads": threads,
            "category": category,
            "category_filter_form": category_filter_form,
        },
    )


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if post.author != request.user:
            Notification.objects.get_or_create(
                sender=request.user,
                receiver=post.author,
                verb=f"{request.user.username} liked your post.",
                content_object=post,
            )
    return redirect("forum:thread_detail", slug=post.thread.slug)


def categories_list(request):
    """
    Display a list of all categories.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    categories = Category.objects.filter(parent__isnull=True).prefetch_related(
        "subcategories"
    )
    return render(request, "forum/categories_list.html", {"categories": categories})


@login_required
def upload_file(request):
    if request.method == "POST" and settings.ALLOW_UPLOADS:
        form = UploadForm(request.POST, request.FILES, initial={"user": request.user})
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.full_clean()
            upload.save()
            messages.success(request, "File uploaded successfully.")
            if is_htmx(request):
                return redirect("forum:existing_uploads_island")
            return redirect("forum:existing_uploads")
        else:
            messages.error(request, "There was an error uploading your file.")
    else:
        form = UploadForm()
    return render(request, "forum/upload_file.html", {"form": form})


@login_required
def existing_uploads(request):
    uploads = Upload.objects.filter(user=request.user).order_by("-uploaded_at")
    total_used_bytes = sum(upload.file.size for upload in uploads if upload.file)
    total_used_mb = round(total_used_bytes / (1024 * 1024), 2)
    quota_mb = settings.SITE_CONFIG["UPLOAD_QUOTA_MB"]

    # Prepare human-readable sizes for each upload
    for u in uploads:
        size = u.file.size
        if size < 1024:
            u.human_size = f"{size} B"
        elif size < 1024 * 1024:
            u.human_size = f"{size/1024:.2f} KB"
        else:
            u.human_size = f"{size/(1024*1024):.2f} MB"

    context = {
        "uploads": uploads,
        "total_used_mb": total_used_mb,
        "quota_mb": quota_mb,
    }
    return render(request, "forum/existing_uploads.html", context)


@login_required
def delete_upload(request, pk):
    upload = get_object_or_404(Upload, pk=pk, user=request.user)
    if request.method == "POST":
        upload.delete()
        messages.success(request, "Upload deleted successfully.")
        return redirect("forum:existing_uploads")
    return render(request, "forum/confirm_delete_upload.html", {"upload": upload})


@csrf_exempt
def link_click(request, pk):
    if request.method == "POST":
        link = Link.objects.get(pk=pk)
        link.clicks += 1
        link.save()
        return JsonResponse({"success": True, "clicks": link.clicks})
    return JsonResponse({"success": False})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        thread_slug = post.thread.slug
        thread = post.thread
        post.delete()
        if not thread.posts.exists():
            thread.delete() # Delete thread too if no posts left
            return redirect("core:frontpage")
        messages.success(request, "Post deleted successfully.")
        return redirect("forum:thread_detail", slug=thread_slug)
    return render(request, "forum/confirm_delete_post.html", {"post": post})