# views.py

import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField


class ForeignKeyAutocompleteView(View):
    def get(self, request):
        app_label = request.GET.get("app_label")
        model_name = request.GET.get("model_name")
        field_name = request.GET.get("field_name")

        if not app_label or not model_name or not field_name:
            error_message = (
                "app_label, model_name, and field_name are required parameters."
            )
            return HttpResponseBadRequest(
                content=json.dumps({"error": error_message}),
                content_type="application/json",
            )
        model = apps.get_model(app_label, model_name)

        if model is None:
            error_message = f"Model {model_name} not found in app {app_label}"
            return HttpResponseBadRequest(
                content=json.dumps({"error": error_message}),
                content_type="application/json",
            )

        try:
            field = model._meta.get_field(field_name)
        except Exception as e:
            error_message = f"Field {field_name} not found in model {model_name}"
            return HttpResponseBadRequest(
                content=json.dumps({"error": error_message}),
                content_type="application/json",
            )

        if isinstance(field, (ForeignKey, OneToOneField, ManyToManyField)):
            term = request.GET.get("term", "")
            related_field_name = (
                f"{field_name}__{field.target_field.name}__icontains"
                if isinstance(field, ForeignKey)
                else f"{field_name}__icontains"
            )
            queryset = model.objects.filter(**{related_field_name: term})[:10]
            results = [{"id": obj.pk, "text": str(obj)} for obj in queryset]
            return JsonResponse({"results": results})
        else:
            error_message = f"Field {field_name} is not a ForeignKey, OneToOneField, or ManyToManyField"
            return HttpResponseBadRequest(
                content=json.dumps({"error": error_message}),
                content_type="application/json",
            )
