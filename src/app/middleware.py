from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


class UserMiddleware(SimpleMiddleware):
    """Basic middleware to add user to request with some non-django authentication methods, like JWT or DRF token"""

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.user = SimpleLazyObject(
                lambda: self.get_user(request) or get_user(request)
            )

        return self.get_response(request)


class JWTAuthMiddleware(UserMiddleware):
    @staticmethod
    def get_user(request):
        json_auth = JWTTokenUserAuthentication()
        try:
            auth = json_auth.authenticate(request)
        except APIException:
            return

        if auth is None:
            return

        return auth[0]


class TokenAuthMiddleware(UserMiddleware):
    @staticmethod
    def get_user(request):
        token_authentication = TokenAuthentication()
        try:
            auth = token_authentication.authenticate(request)
        except APIException:
            return

        if auth is None:
            return

        return auth[0]
