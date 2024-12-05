from django.shortcuts import render, redirect, get_object_or_404
from apps.account.models import User
from django.contrib import messages
from apps.core.templatetags.convert_markdown import convert_markdown
from apps.account.templatetags.user_mention import user_mention

from django.contrib.auth.decorators import login_required
from apps.account.forms import (
    UserEditForm,
    UserProfileForm,
    UserProfileAvatarForm,
    UserRegisterForm,
)


def signup(request):
    """
        View to handle user registration and account creation.

        Args:
            request: The HTTP request.

    Returns:
            HttpResponse: A response with the registration form or a redirect to the login page.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("account:login")
    form = UserRegisterForm()
    return render(request, "registration/signup.html", {"form": form})


def user_detail(request, username):
    """
    View to display user profile details, posts, and replies.

    Args:
        request: The HTTP request.
        username (str): The username of the user to display.

    Returns:
        HttpResponse: A response with the user profile details, posts, and replies.
    """
    tuser = get_object_or_404(User, username=username)
    tuser_threads = tuser.threads.all()[:5]
    tuser_replies = tuser.posts.filter(parent__isnull=False)[:5]
    context = {
        "tuser": tuser,
        "tuser_threads": tuser_threads,
        "tuser_replies": tuser_replies,
    }
    return render(request, "account/user_detail.html", context)


@login_required
def user_preference(request, username):
    """
    View to handle user preferences and profile updates.

    Args:
        request: The HTTP request.
        username (str): The username of the user whose preferences are being updated.

    Returns:
        HttpResponse: A response with the user's profile preferences form.
    """
    if username != request.user.username:
        return redirect("account:user_detail", username=username)
    tuser = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        uform = UserEditForm(request.POST, instance=tuser)
        pform = UserProfileForm(request.POST, instance=tuser.userprofile)
        aform = UserProfileAvatarForm(
            request.POST, request.FILES, instance=tuser.userprofile
        )
        if uform.is_valid() and pform.is_valid() and aform.is_valid():
            uform.save()
            pform.save()
            aform.save()
            messages.success(request, f"Preference updated for {username}!")
            return redirect("account:user_preference", username=username)
    uform = UserEditForm(instance=tuser)
    pform = UserProfileForm(instance=tuser.userprofile)
    aform = UserProfileAvatarForm(instance=tuser.userprofile)
    return render(
        request,
        "account/user_preference.html",
        {"tuser": tuser, "pform": pform, "aform": aform, "uform": uform},
    )
