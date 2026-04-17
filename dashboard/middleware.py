"""
dashboard/middleware.py

Allows Home Assistant and other external clients to authenticate
using a static Bearer token instead of Django session cookies.

Token is set in settings.py:
    DASHBOARD_API_TOKEN = "iscar-token-2026"
"""

from django.conf import settings


class BearerTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
            expected = getattr(settings, "DASHBOARD_API_TOKEN", None)
            if expected and token == expected:
                request._api_token_valid = True
        return self.get_response(request)
