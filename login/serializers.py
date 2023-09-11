from users.models import User
from rest_framework import serializers


class AuthUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=250, required=True)
    password = serializers.CharField(max_length=250, required=True)

    class Meta:
        model = User
        fields = "__all__"


class LogoutTokenSerializer(serializers.Serializer):
    token = serializers.CharField(label="token", default=None, required=False)