from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["pk", "name"]
    list_editable = ["name"]
    ordering = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ["author", "categories", "likes", "reply_to"]
    list_display = ["pk", "title", "author", "status", "created_at", "updated_at"]
    list_editable = ["title", "status"]
    actions = ["make_publish"]
    list_filter = ["status", "created_at", "updated_at"]

    @admin.action(description="Mark selected posts as published")
    def make_publish(self, request, queryset):
        queryset.update(status="Published")
        self.message_user(request, "Selected posts are marked as published")
