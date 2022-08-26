from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):

        """
        Read the authorization header, verify token, and authenticate credentials.
        """

        request.user = None
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            return None

        prefix, token = authorization_header.split(" ")

        if prefix != settings.TOKEN_TYPE:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, access_token):

        """
        A helper function decodes JWT token and verifies the User.
        Output is tuple of (user, access_token).
        """

        try:
            payload = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access_token expired")
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")

        user = User.objects.filter(id=payload["sub"]).first()

        if not user:
            raise exceptions.AuthenticationFailed("User not found")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        return user, access_token
