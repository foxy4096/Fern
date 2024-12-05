from django.shortcuts import render, get_object_or_404, resolve_url
from .forms import ReplyCreationForm
from apps.core.utils import paginate, is_hx_paginated
from django.contrib.auth.decorators import login_required

from .models import Post, Thread

@login_required
def reply_form(request, pk):
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