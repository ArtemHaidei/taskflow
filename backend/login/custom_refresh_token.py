from rest_framework_simplejwt.tokens import Token, AccessToken
from django.conf import settings
from typing import Any, Dict

from rest_framework_simplejwt.exceptions import TokenError
from taskflow.redis_db import RedisConnectionDB


class BlacklistMixin:
    """
    Custom Mixin that adds blacklist methods to a token.
    Redis is used as a database for storing tokens.
    """
    payload: Dict[str, Any]
    redis_db = RedisConnectionDB(db=settings.REDIS_TOKENS_DB)

    def verify(self, *args, **kwargs) -> None:
        self.check_blacklist()

    def check_blacklist(self) -> None:
        """
        Verifies whether this token exists in the token blacklist and raises a TokenError if it does.
        """
        jti = self.payload[settings.SIMPLE_JWT["JTI_CLAIM"]]
        if self.redis_db.check_jti(jti):
            raise TokenError("Token is in blacklist")

    def blacklist(self) -> None:
        """
        Verifies the token's absence from the blacklist; if found, a TokenError is raised.
        Otherwise, the token is added to the blacklist.
        """
        jti = self.payload[settings.JTI_CLAIM]
        exp = self.payload["exp"]

        if self.redis_db.check_jti(jti):
            raise TokenError("Token is in blacklist")

        self.redis_db.setex_jti(jti, exp, self.payload["user_id"])


class RefreshToken(BlacklistMixin, Token):
    """
    Custom Refresh Token
    """
    token_type = "refresh"
    lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    no_copy_claims = (
        settings.SIMPLE_JWT['TOKEN_TYPE_CLAIM'],
        "exp",
        settings.SIMPLE_JWT['JTI_CLAIM'],
        "jti",
    )

    access_token_class = AccessToken

    @property
    def access_token(self) -> AccessToken:
        access = self.access_token_class()
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access
