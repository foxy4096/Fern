from django import forms
from .models import Post, Thread

from apps.core.widgets import MarkdownWidget


class ThreadCreationForm(forms.ModelForm):
    """
    Form for creating a new Thread.
    """

    class Meta:
        model = Thread
        fields = [
            "title",
            "category",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "is-large",
                    "_": "on keyup if value of me is empty then add .is-danger else remove .is-danger",
                }
            ),
        }


class PostCreationForm(forms.ModelForm):
    """
    Form for creating a new post.
    """

    class Meta:
        model = Post
        fields = ["body", "status"]
        widgets = {
            "body": MarkdownWidget(),
        }


class ReplyCreationForm(forms.ModelForm):
    """
    Form for creating a new reply.
    """

    class Meta:
        model = Post
        fields = [
            "body",
        ]
        widgets = {
            "body": MarkdownWidget(),
        }
