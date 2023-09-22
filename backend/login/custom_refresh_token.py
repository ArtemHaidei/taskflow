import time

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.conf import settings
from typing import Any, Dict

from rest_framework_simplejwt.exceptions import TokenError
from taskflow.redis_db import RedisConnectionDB


class CustomBlacklistMixin:
    """
    Custom Mixin that adds blacklist methods to a token.
    Redis is used as a database for storing tokens.
    """
    payload: Dict[str, Any]

    def verify(self) -> bool:
        return not self.check_blacklist()

    def check_blacklist(self) -> bool:
        """
        Verifies whether this token exists in the token blacklist and raises a TokenError if it does.
        """
        client = RedisConnectionDB()
        jti = self.payload[settings.SIMPLE_JWT["JTI_CLAIM"]]
        if client.check_jti(jti):
            return True
        return False

    def blacklist(self) -> None:
        """
        Verifies the token's absence from the blacklist; if found, a TokenError is raised.
        Otherwise, the token is added to the blacklist.
        """
        client = RedisConnectionDB()
        jti = self.payload[settings.JTI_CLAIM]

        if client.check_jti(jti):
            raise TokenError("Token is in blacklist")

        exp = self.payload["exp"]

        current_time = int(time.time())
        time_to_live = int(exp) - current_time
        user_id = int(self.payload["user_id"])

        client.setex_jti(jti, time_to_live, user_id)

    @classmethod
    def for_user(cls):
        pass


class CustomAccessToken(AccessToken, CustomBlacklistMixin):
    """
    Custom Access Token with blacklist support
    """


class CustomRefreshToken(RefreshToken, CustomBlacklistMixin):
    """
    Custom Refresh Token
    """
    access_token_class = CustomAccessToken
