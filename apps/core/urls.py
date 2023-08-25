from django.views.generic import TemplateView
from django.urls import path

app_name = "core"
urlpatterns = [
    path(
        "", TemplateView.as_view(template_name="core/frontpage.html"), name="frontpage"
    ),
]
