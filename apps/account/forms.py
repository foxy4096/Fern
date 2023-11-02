from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, User
from apps.core.widgets import MarkdownWidget


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Required.", label="First Name"
    )
    last_name = forms.CharField(
        max_length=30, required=False, help_text="Optional.", label="Last Name"
    )
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")

        if commit:
            user.save()

        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information, including a bio with live Markdown conversion.

    Usage:
        This form is used to edit user profile information. It includes a bio field with live Markdown conversion.

        Example:
        ```
        form = UserProfileForm(
            rendered_initials="Your rendered bio content here"
        )
        ```

    Attributes:
    """

    class Meta:
        model = UserProfile
        fields = ["location", "website", "bio", "use_gravtar"]
        widgets = {
            "bio": MarkdownWidget(),
        }


class UserProfileAvatarForm(forms.ModelForm):
    """
    Form for updating user profile avatar.

    Usage:
        This form is used to update the user's profile avatar.

        Example:
        ```
        form = UserProfileAvatarForm()
        ```
    """

    class Meta:
        model = UserProfile
        fields = ["avatar", "header"]
