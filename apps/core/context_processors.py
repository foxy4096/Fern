from django.conf import settings


def is_htmx(request):
    return {"is_htmx": request.META.get("Hx-Request") == "true"}

def core_config(request):
    return settings.SITE_CONFIG

def site_title(request):
    return {"site_title": settings.SITE_TITLE}