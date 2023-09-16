from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class AuthUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])


class LogoutTokenSerializer(serializers.Serializer):
    token = serializers.CharField(label="token", default=None, required=False)