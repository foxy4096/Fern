from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.redirects.admin import RedirectAdmin as BaseRedirectAdmin
from django.contrib.redirects.models import Redirect


# This file serves as the Base Configuration for the Admin Panel.


class RedirectAdmin(BaseRedirectAdmin):
    list_display = ("old_path", "new_path")
    list_filter = ("site",)
    list_select_related = ("site",)
    autocomplete_fields = ["site"]


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ("app_label", "model")
    ordering = ("app_label", "model")


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_per_page = 10
    autocomplete_fields = ["content_type", "user"]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_per_page = 10
    autocomplete_fields = ["content_type"]
    search_fields = ("name",)


admin.site.unregister(Redirect)
admin.site.register(Redirect, RedirectAdmin)


admin.site.site_header = settings.ADMIN_SITE_TITLE
admin.site.site_title = settings.ADMIN_SITE_TITLE
