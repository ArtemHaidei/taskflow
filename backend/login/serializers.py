import time
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import UntypedToken
from login.custom_refresh_token import RefreshToken
from taskflow.redis_db import RedisConnectionDB


class AuthUserTokenPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(required=True)


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate(self, data):
        token = UntypedToken(token=data["token"], verify=True)
        jti = token.get(settings.SIMPLE_JWT["JTI_CLAIM"])

        redis_db = RedisConnectionDB(db=settings.REDIS_TOKENS_DB)

        if redis_db.check_jti(jti):
            raise serializers.ValidationError("Token is in blacklist")

        return {}


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs) -> dict[str, str]:
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        data["refresh"] = str(refresh)

        return data


