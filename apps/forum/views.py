from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url

from apps.forum.forms import (
    PostCreationForm,
    ReplyCreationForm,
    ThreadCreationForm,
    CategoryFilterForm,
)
from apps.forum.models import Post, Thread, Category
from .islands import thread_post_list
from apps.core.utils import paginate

from apps.core.utils import is_htmx


@login_required
def thread_create(request):
    """
    Create a new thread and handle form submissions.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    tform = ThreadCreationForm(request.POST if request.method == "POST" else None)
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
        {"threads": threads, "category": category, "category_filter_form": category_filter_form},
    )


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("forum:thread_detail", slug=post.thread.slug)
