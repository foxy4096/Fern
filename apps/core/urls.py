from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.FrontpageView.as_view(), name="frontpage"),
    path("home/", views.HomeView.as_view(), name="homepage"),
    path(
        "convert/md/", views.convert_markdown_to_html, name="convert_markdown_to_html"
    ),
    path("search/", views.search, name="search"),
]
