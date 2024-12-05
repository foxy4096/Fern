from django import forms
from .models import Post, Thread, Category

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
            # "category": AutoCompleteWidget(lookup_url="/auto/some", lookup_fields=["title"]),
        }


class CategoryCreationForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True), required=False
    )

    def __init__(self, *args, **kwargs):
        super(CategoryCreationForm, self).__init__(*args, **kwargs)
        self.fields["parent"].queryset = Category.objects.filter(parent__isnull=True)

    class Meta:
        model = Category
        fields = ["name", "description", "parent", "slug", "color"]
        


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


class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=True),
        to_field_name="slug",
        widget=forms.Select(attrs={
            "onchange": "window.location = '/forum/c/' + document.querySelector('#id_category').value + '/';",
        })
    )
    subcategory = forms.ModelChoiceField(
        queryset=Category.objects.filter(parent__isnull=False),
        to_field_name="slug",
        widget=forms.Select(attrs={
            "onchange": "window.location = '/forum/c/' + document.querySelector('#id_subcategory').value + '/';",
        })
    )

    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args, **kwargs)
        # Get the subcategory by the parent category children
        category = kwargs.get("initial", {}).get("category", None)
        self.fields["subcategory"].queryset = Category.objects.filter(parent=category)

