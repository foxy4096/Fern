from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from apps.core.utils import paginate
from django.contrib.auth.decorators import login_required

@login_required
def notification_page(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by('-created_at')
    notifications = paginate(request, notifications, limit=20)
    return render(request, 'notification/notification_page.html', {'notifications': notifications})


@login_required
def redirect_to_notification_target(request, pk):
    notification = get_object_or_404(Notification, pk=pk, receiver=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.content_object.get_absolute_url())