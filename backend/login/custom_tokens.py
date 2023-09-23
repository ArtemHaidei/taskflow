import time
from typing import Any

from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, UntypedToken

from taskflow.redis_db import RedisConnectionDB


class CustomBlacklistMixin:
    """Custom Mixin that adds blacklist methods to a token.

    Redis is used as a database for storing tokens.
    """

    payload: dict[str, Any]

    def verify(self) -> bool:
        return not self.check_blacklist()

    def check_blacklist(self) -> bool:
        """Verify whether this token exists in the token blacklist.

        Raises a TokenError if it does.
        """
        client = RedisConnectionDB()
        jti = self.payload[settings.SIMPLE_JWT["JTI_CLAIM"]]
        if client.check_jti(jti):
            return True
        return False

    def blacklist(self) -> None:
        """Verify the token's absence from the blacklist.

        If found, a TokenError is raised.

        Otherwise, the token is added to the blacklist.
        """
        client = RedisConnectionDB()
        jti = self.payload[settings.SIMPLE_JWT["JTI_CLAIM"]]

        if client.check_jti(jti):
            msg = (
                f"{self.payload[settings.SIMPLE_JWT['TOKEN_TYPE_CLAIM']]} "
                "token is in blacklist"
            )
            raise TokenError(
                msg)

        exp = self.payload["exp"]

        current_time = int(time.time())
        time_to_live = int(exp) - current_time
        user_id = int(self.payload["user_id"])

        client.setex_jti(jti, time_to_live, user_id)

    @classmethod
    def for_user(cls, user):
        """Rewrite for_user."""
        return super().for_user(user)  # type: ignore


class CustomAccessToken(AccessToken, CustomBlacklistMixin):
    """Rewrite Access Token with blacklist support."""


class CustomRefreshToken(CustomBlacklistMixin, RefreshToken):
    """Rewrite Refresh Token."""

    access_token_class = CustomAccessToken


class CustomUntypedToken(CustomBlacklistMixin, UntypedToken):
    """Rewrite Untyped Token."""
