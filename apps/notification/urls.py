from django.urls import path
from . import views

app_name = "notification"
urlpatterns = [
    # Other URL patterns
    path("", views.notification_page, name="notification_page"),
    path("<int:pk>/redirect/", views.redirect_to_notification_target, name="redirect_to_notification_target"),
]
