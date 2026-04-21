from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth = JWTAuthentication()

    def __call__(self, request):

        access = request.COOKIES.get("access")

        if access:
            try:
                token = self.auth.get_validated_token(access)
                request.user = self.auth.get_user(token)
                request.auth = token
            except TokenError:
                request.user = AnonymousUser()

            except Exception:
                request.user = AnonymousUser()

        else:
            request.user = AnonymousUser()
        
        return self.get_response(request)