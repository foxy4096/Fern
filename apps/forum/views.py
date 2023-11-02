from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url

from apps.forum.forms import PostCreationForm, ReplyCreationForm, ThreadCreationForm
from apps.forum.models import Post, Thread
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
        return redirect("forum:thread_detail", pk=thread.pk)
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


def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if is_htmx(request):
        return thread_post_list(request, pk)
    posts = paginate(request, thread.posts.all())
    return render(
        request,
        "forum/thread_detail.html",
        {"thread": thread, "posts": posts},
    )


def post_detail(request, thread_pk, post_pk):
    """
    Display the details of a post and provide a form for creating replies.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the post to display.

    Returns:
        HttpResponse: The rendered HTML response.
    """
    thread = get_object_or_404(Thread, pk=thread_pk)
    post = get_object_or_404(thread.posts.all(), pk=post_pk)
    return render(request, "forum/post_detail.html", {"post": post})


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
            return redirect("forum:thread_detail", pk=post.thread.pk)
        else:
            messages.error(request, "There was an error in your reply creation.")
    else:
        form = ReplyCreationForm()

    return render(
        request, "forum/reply_create.html", {"reply_form": form, "post": post}
    )
