from django.urls import path, include
from . import views

app_name = "account"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.signup, name="signup"),
    path("user/<str:username>/", views.user_detail, name="user_detail"),
    path("user/<str:username>/preference/", views.user_preference, name="user_preference"),
]
