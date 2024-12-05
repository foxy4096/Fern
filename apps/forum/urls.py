from django.urls import path
from . import views, islands
from django.views.generic import RedirectView

app_name = "forum"

urlpatterns = [
    path("create/", views.thread_create, name="thread_create"),
    path("t/<slug:slug>/", views.thread_detail, name="thread_detail"),
    path("t/<slug:thread_slug>/<int:post_pk>", views.post_detail, name="post_detail"),
    # Post edit
    path("<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("<int:pk>/reply/", views.reply_create, name="reply_create"),

    path('c/<str:slug>/', views.threads_by_category, name='threads_by_category'),
    path('c//', RedirectView.as_view(url='/home')),

    # Islands
    path("islands/reply/<int:pk>/", islands.reply_form, name="reply_form"),
    path('islands/threads/<int:pk>/', islands.thread_post_list, name='thread_post_list'),
    path('islands/threads/<int:pk>/reply-button/', islands.reply_button, name='reply_button'),
    path('islands/threads/<int:pk>/post-block/', islands.post_block, name='post_block'),
]
