from apps.core.utils import get_user_agent, get_user_ip

from .models import UserSession


class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            context = {
                "user": request.user,
                "session_id": request.session.session_key,
                "ip_address": get_user_ip(request),
                "user_agent": get_user_agent(request),
            }
            UserSession.objects.get_or_create(**context)

        return self.get_response(request)
