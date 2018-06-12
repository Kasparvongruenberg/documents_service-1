from django.conf import settings
from rest_framework.permissions import IsAuthenticated


class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        if getattr(request, 'session', None) and \
                request.session.get('jwt_iss') == settings.JWT_ALLOWED_ISSUER:
            return True

        return request.user and request.user.is_authenticated
