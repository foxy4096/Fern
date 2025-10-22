from django import forms
from .models import Post, Thread, Category, Upload
from apps.core.widgets import MarkdownWidget


class ThreadCreationForm(forms.ModelForm):
    """
    Form for creating a new Thread.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set category placeholder
        self.fields["category"].required = True
        self.fields["category"].empty_label = "Select a category"

        # If instance is not set, check for initial category and apply it
        if not self.instance.pk:
            initial_category = self.initial.get("category")
            if initial_category:
                self.fields["category"].initial = initial_category

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


class CategoryCreationForm(forms.ModelForm):
    # parent = forms.ModelChoiceField(
    #     queryset=Category.objects.filter(parent__isnull=True), required=False
    # )

    # def __init__(self, *args, **kwargs):
    #     super(CategoryCreationForm, self).__init__(*args, **kwargs)
    #     self.fields["parent"].queryset = Category.objects.filter(parent__isnull=True)

    class Meta:
        model = Category
        fields = ["name", "description", "parent", "slug", "color"]


class PostCreationForm(forms.ModelForm):
    """
    Form for creating a new post.
    """

    class Meta:
        model = Post
        fields = ["body",]
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
    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop("path", [])  # slugs like ["programming", "python"]
        super().__init__(*args, **kwargs)

        parent = None
        for i, slug in enumerate(self.path):
            try:
                parent = Category.objects.get(slug=slug, parent=parent)
            except Category.DoesNotExist:
                break

        next_categories = Category.objects.filter(parent=parent)

        if next_categories.exists():
            self.fields[f"level_{len(self.path)}"] = forms.ModelChoiceField(
                queryset=next_categories,
                to_field_name="slug",
                required=True,
                label="Select category",
                widget=forms.Select(
                    attrs={
                        "hx-get": "/forum/category-filter/",
                        "hx-target": "#category-chain",
                        "hx-include": "closest form",
                        "hx-push-url": "true",
                    }
                ),
            )


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ["file", "description"]

    def clean(self):
        cleaned_data = super().clean()
        self.instance.user = self.initial.get("user")  # set current user if needed
        self.instance.clean()  # manually trigger model clean
        return cleaned_data