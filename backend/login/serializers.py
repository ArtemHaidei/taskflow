from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AuthUserSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(required=True)


class LogoutTokenSerializer(serializers.Serializer):
    token = serializers.CharField(label="token", default=None, required=False)