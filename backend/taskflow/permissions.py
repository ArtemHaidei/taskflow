from django.conf import settings
from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import UntypedToken

from taskflow.redis_db import RedisConnectionDB


class CustomAPIException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {"message": "Access token in the blacklist."} # noqa


class IsNotBlacklisted(permissions.BasePermission):
    def has_permission(self, request, view):  # noqa
        raw_token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]
        untyped_token = UntypedToken(raw_token)
        client = RedisConnectionDB()

        if client.check_jti(untyped_token.payload[settings.SIMPLE_JWT["JTI_CLAIM"]]):
            raise CustomAPIException

        return True
