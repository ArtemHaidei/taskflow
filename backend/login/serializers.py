from rest_framework import serializers


class AuthUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=250, required=True)
    password = serializers.CharField(max_length=250, required=True)


class LogoutTokenSerializer(serializers.Serializer):
    token = serializers.CharField(label="token", default=None, required=False)