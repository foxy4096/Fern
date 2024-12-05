from django.urls import path
from . import views
from . import islands

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.poll_create, name="poll_create"),
    path('my-polls/', views.my_polls, name="my_polls"),
    path('view/<int:pk>/', views.poll_detail, name='poll_detail'),
    path('edit/<int:pk>/', views.poll_edit, name='poll_edit'),
    path('edit/<int:pk>/add-choice/', views.poll_choice_create, name='poll_choice_create'),
    path('delete-choice/<int:pk>/', views.poll_choice_delete, name='poll_choice_delete'),
    path('delete/<int:pk>/', views.poll_delete, name='poll_delete'),
    path('vote/<int:pk>/', views.vote, name='poll_vote'),


    # Islands
    path('create/choice/', islands.choice_create, name="choice_create"),
]
