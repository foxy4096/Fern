from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url
from .models import User, UserPreference, UserProfile, UserSession
from django.contrib.sessions.models import Session


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
        "username",
        "profile_picture",
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


class UserSessionInline(admin.StackedInline):
    """Stacked Inline View for UserSession"""

    model = UserSession
    autocomplete_fields = ["user"]
    can_delete = False


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = [UserSessionInline]
    list_display = ("session_key", "expire_date", "display_user")

    @admin.display(description="User")
    def display_user(self, obj):
        return user_display_link_html(obj.usersession.user)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
