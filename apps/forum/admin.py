from django.contrib import admin
from django.db import models
from .models import Category, Post, Thread
from .forms import CategoryCreationForm
from apps.core.widgets import MarkdownWidget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]
    list_per_page = 10
    ordering = ["name"]
    list_display = ["name", "slug", "color", "parent"]
    list_display_links = ["slug"]
    list_editable = ["name", "color", "parent"]
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ['parent']
    form = CategoryCreationForm


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "creator", "is_locked"]
    list_filter = ["created_at", "is_locked"]
    list_select_related = True
    search_fields = ["catrgory", "creator__username", "title"]
    actions = ["lock_thread", "unlock_thread"]
    autocomplete_fields = ["creator", "category"]
    prepopulated_fields = {"slug": ("title",)}

    @admin.action(description="Lock selected threads")
    def lock_thread(self, request, queryset):
        queryset.update(is_locked=True)
        self.message_user(request, "Selected threads are locked")

    @admin.action(description="Unlock selected threads")
    def unlock_thread(self, request, queryset):
        queryset.update(is_locked=False)
        self.message_user(request, "Selected threads are unlocked")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ["body", "author__username", "thread__title"]
    formfield_overrides = {models.TextField: {"widget": MarkdownWidget()}}
    autocomplete_fields = ["author", "likes", "parent", "thread"]
    list_select_related = True
    list_display = ["__str__", "author", "status", "created_at", "updated_at"]
    list_per_page = 10
    list_editable = ["status"]
    actions = ["make_publish"]
    list_filter = ["status", "created_at", "updated_at"]

    @admin.action(description="Mark selected posts as published")
    def make_publish(self, request, queryset):
        queryset.update(status="Published")
        self.message_user(request, "Selected posts are marked as published")
