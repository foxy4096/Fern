from django import template
from django.urls import reverse
from ..models import User
import re

register = template.Library()


@register.filter
def user_mention(value):
    return re.sub(r"@(\w+)", replace_mention, value)


def replace_mention(match):
    username = match.group(1)
    if user := User.objects.filter(username=username).first():
        profile_url = reverse("account:user_detail", args=[username])
        return f"""<a href="{profile_url}" class="user-mention tag is-dark" title="{username}">
            <span class="icon">
                <img src="{user.userprofile.avatar_image()}" class="user-mention-image" alt="{username}'s Avatar" lazy>
            </span>
            <span class="is-link">@{username}</span>
        </a>"""
    return match.group(0)
