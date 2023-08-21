from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from .models import User, UserPreference, UserProfile

avatar_display_html = lambda url: mark_safe(
    f'<img src="{url}" width="80px" style="border-radius: 10px" />'
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    fieldsets = (
        (
            "User Profile",
            {
                "fields": [
                    "bio",
                    "avatar",
                    "profile_picture",
                ]
            },
        ),
    )
    readonly_fields = ["profile_picture"]

    @admin.display(description="Profile Picture")
    def profile_picture(self, obj):
        return avatar_display_html(obj.avatar.url)


class UserPreferenceInline(admin.StackedInline):
    model = UserPreference
    can_delete = False
    extra = 0

    fieldsets = (
        (
            "Email Notifications",
            {
                "fields": ("email_notifications", "email_notifications_frequency"),
            },
        ),
    )


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserPreferenceInline)
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

    @admin.display(description="Profile Picture")
    def profile_picture(self, obj):
        return avatar_display_html(obj.userprofile.avatar.url)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
