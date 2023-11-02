from django.core.paginator import Paginator


def is_htmx(request, boost_check=True):
    hx_boost = request.headers.get("Hx-Boosted")
    hx_request = request.headers.get("Hx-Request")
    if boost_check:
        if hx_boost:
            return False

        elif hx_request:
            return True


is_hx_paginated = lambda request: request.headers.get("Hx-Paginated") == "true"


def paginate(request, qs, limit=5):
    paginated_qs = Paginator(qs, limit, orphans=5)
    page_no = request.GET.get("page")
    return paginated_qs.get_page(page_no)


def get_user_ip(request):
    return (
        x_forwarded_for.split(",")[0]
        if (x_forwarded_for := request.META.get("HTTP_X_FORWARDED_FOR"))
        else request.META.get("REMOTE_ADDR")
    )


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT")
