from django.shortcuts import render
from .models import Notification

def notification_page(request):
    notifications = Notification.objects.all()
    return render(request, 'notification/notification_page.html', {'notifications': notifications})
