from django.urls import path
from . import views, islands

app_name = "forum"

urlpatterns = [
    path("create/", views.thread_create, name="thread_create"),
    path("<int:pk>/", views.thread_detail, name="thread_detail"),
    path("<int:thread_pk>/<int:post_pk>", views.post_detail, name="post_detail"),
    path("<int:pk>/reply/", views.reply_create, name="reply_create"),

    # Islands
    path("islands/reply/<int:pk>/", islands.reply_form, name="reply_form"),
    path('islands/threads/<int:pk>/', islands.thread_post_list, name='thread_post_list'),
    path('islands/threads/<int:pk>/reply-button/', islands.reply_button, name='reply_button'),
]
