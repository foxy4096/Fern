# urls.py

from django.urls import path
from .views import ForeignKeyAutocompleteView

urlpatterns = [
    path("", ForeignKeyAutocompleteView.as_view(), name="autocomplete"),
]
