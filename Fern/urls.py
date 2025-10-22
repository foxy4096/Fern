from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("polls/", include("apps.polls.urls")),
    path("forum/", include("apps.forum.urls")),
    path("accounts/", include("apps.account.urls")),
    path("accounts/", include("apps.account.admin_urls")),
    path("notifications/", include("apps.notification.urls")),
    path("", include("user_sessions.urls", "user_sessions")),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
