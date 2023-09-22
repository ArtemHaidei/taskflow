from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings
from taskflow.redis_db import RedisConnectionDB


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        if self.is_token_blacklisted(validated_token):
            raise exceptions.AuthenticationFailed('Access token in the blacklist.')

        return self.get_user(validated_token), validated_token

    @staticmethod
    def is_token_blacklisted(validated_token):
        client = RedisConnectionDB()
        return client.check_jti(validated_token.payload[settings.SIMPLE_JWT["JTI_CLAIM"]])
