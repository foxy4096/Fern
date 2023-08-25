from django.urls import path, include

app_name = "account"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
