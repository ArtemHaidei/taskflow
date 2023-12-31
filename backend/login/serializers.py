from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from login.custom_tokens import (
    CustomAccessToken,
    CustomRefreshToken,
    CustomUntypedToken,
)


class AuthUserTokenPairSerializer(TokenObtainPairSerializer):
    token_class = CustomRefreshToken

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"] = serializers.EmailField(required=True)


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate(self, data) -> dict:
        token = CustomUntypedToken(token=data["token"], verify=True)
        if token.check_blacklist():
            return {"message": "Token is in blacklist"}

        return {"message": "Token is valid."}


class TokenLogoutSerializer(serializers.Serializer):
    access = serializers.CharField(required=True)
    refresh = serializers.CharField()

    def validate(self, data) -> dict[str, str]:
        response = {
                "message": "Successfully logged out.",
                "access": "Access token is added to blacklist.",
                "refresh": "Refresh token is added to blacklist.",
            }

        access = CustomAccessToken(data["access"])
        access.blacklist()

        refresh_token = data.get("refresh", None)
        if not refresh_token:
            response["refresh"] = "Refresh token is required."
            return data

        refresh = CustomRefreshToken(refresh_token)
        if not refresh.check_blacklist():
            refresh.blacklist()
            return response

        response["refresh"] = "Refresh token is already in blacklist."
        return response


class TokenAccessRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    token_class = CustomRefreshToken

    def validate(self, data) -> dict[str, str]:
        refresh = self.token_class(data["refresh"])

        if refresh.check_blacklist():
            return {"message": "Refresh token is in blacklisted."}

        return {"access": str(refresh.access_token)}
