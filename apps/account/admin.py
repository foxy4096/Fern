from django.contrib import admin
from apps.core.widgets import MarkdownWidget
from django.db import models

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url
from .models import User, UserProfile


avatar_display_html = lambda url: mark_safe(
    f'<img src="{url}" width="30px" style="border-radius: 100px" />'
)

user_display_link_html = lambda obj: mark_safe(
    f'<a href="{resolve_url("admin:auth_user_change", obj.id)}">{obj.username}</a>'
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    formfield_overrides = {models.TextField: {"widget": MarkdownWidget()}}
    fieldsets = (
        (
            "User Profile",
            {
                "fields": [
                    "bio",
                    "avatar",
                    "use_gravtar",
                    "profile_picture",
                    "header",
                    "location",
                    "website",
                ]
            },
        ),
    )
    readonly_fields = ["profile_picture"]

    @admin.display(description="Avatar")
    def profile_picture(self, obj):
        return avatar_display_html(obj.avatar_image())



class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "profile_picture",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_display_links = ("profile_picture", "username")
    ordering = ["username"]

    @admin.display(description="Avatar")
    def profile_picture(self, obj):
        return avatar_display_html(obj.userprofile.avatar_image())


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
