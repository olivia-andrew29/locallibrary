from django.contrib.auth import get_user_model
from ninja.security import HttpBearer

from .tokens import decode_token


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        claims = decode_token(token, "access")

        if claims is None:
            return None

        User = get_user_model()

        try:
            return User.objects.get(id=int(claims["sub"]))
        except (User.DoesNotExist, ValueError, TypeError):
            return None