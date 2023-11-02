from django.conf import settings


def is_htmx(request):
    return {"is_htmx": request.META.get("Hx-Request") == "true"}

def core_config(request):
    return settings.NAVBAR_CONFIG