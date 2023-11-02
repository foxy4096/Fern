from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    '''Admin View for Notification'''

    autocomplete_fields = ['sender', 'receiver']