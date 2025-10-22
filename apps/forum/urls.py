from django.urls import path
from . import views, islands

app_name = "forum"

urlpatterns = [
    path("create/", views.thread_create, name="thread_create"),
    path("create/<str:category_slug>/", views.thread_create, name="thread_create"),
    path("t/<slug:slug>/", views.thread_detail, name="thread_detail"),
    path("t/<slug:thread_slug>/<int:post_pk>", views.post_detail, name="post_detail"),
    # Post edit
    path("<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("<int:pk>/reply/", views.reply_create, name="reply_create"),
    path("<int:pk>/delete/", views.delete_post, name="delete_post"),

    path('c/<str:slug>/', views.threads_by_category, name='threads_by_category'),
    path('c/', views.categories_list, name='categories_list'),

    # Islands
    path("islands/reply/<int:pk>/", islands.reply_form, name="reply_form"),
    path("islands/like/<int:pk>/", islands.like_post, name="like_post"),
    path('islands/threads/<int:pk>/', islands.thread_post_list, name='thread_post_list'),
    path('islands/threads/<int:pk>/reply-button/', islands.reply_button, name='reply_button'),
    path('islands/threads/<int:pk>/post-block/', islands.post_block, name='post_block'),
    path('islands/category-filter/', islands.category_filter, name='category_filter'),

    # Upload
    path("upload/", views.upload_file, name="upload_file"),  # New upload path
    path('islands/upload-modal/', islands.upload_modal, name='upload_modal'),
    path('islands/upload-form/', islands.upload_form, name='upload_form'),
    path('islands/existing-uploads/', islands.existing_uploads, name='existing_uploads_island'),
    path('islands/close-modal/', islands.close_modal, name='close_modal'),
    path('islands/insert-upload/<int:pk>/', islands.insert_upload, name='insert_upload'),

    path("uploads/", views.existing_uploads, name="existing_uploads"),  # New existing uploads path
    path("uploads/<int:pk>/delete/", views.delete_upload, name="delete_upload"),

    path('link/<int:pk>/click/', views.link_click, name='link_click')


]
