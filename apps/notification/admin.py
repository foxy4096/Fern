from django.contrib import admin

from .models import Notification, NotificationItem


class NotificationItemInline(admin.StackedInline):
    '''Stacked Inline View for NotificationItem'''

    model = NotificationItem
    autocomplete_fields = ['content_type']
    extra = 0

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    '''Admin View for Notification'''

    inlines = [
        NotificationItemInline,
    ]
    autocomplete_fields = ['sender', 'receiver']