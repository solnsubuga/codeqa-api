import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from authentication.identity import IdentityManager


class JWTAuthentication(authentication.BaseAuthentication):
    """Authentication backend
    """

    def authenticate(self, request):
        token = authentication.get_authorization_header(
            request).decode('utf-8')
        if not token:
            return None
        try:
            token = token.split(' ')[1]
            identity_model = IdentityManager()
            payload = identity_model.decode(token)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e.__str__())
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User does not exist')
        return user, token
