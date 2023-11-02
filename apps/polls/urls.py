from django.urls import path
from . import views
from . import islands

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.poll_create, name="poll_create"),
    path('my-polls/', views.my_polls, name="my_polls"),
    path('view/<int:pk>/', views.poll_detail, name='poll_detail'),

    # Islands
    path('create/choice/', islands.choice_create, name="choice_create"),
]
