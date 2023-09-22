import time

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from login.serializers import (TokenVerifySerializer,
                               AuthUserTokenPairSerializer,
                               TokenRefreshSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from taskflow.redis_db import RedisConnectionDB
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class CustomTokenVerifyView(generics.GenericAPIView):
    serializer_class = TokenVerifySerializer


class UserLoginTokenPairView(TokenObtainPairView):
    serializer_class = AuthUserTokenPairSerializer


class UserLogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenVerifySerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_db = RedisConnectionDB(db=getattr(settings, 'REDIS_TOKENS_DB', 0))

    def add_to_blacklist(self, token):
        current_time = int(time.time())
        time_to_live = int(token.get("exp")) - current_time
        jti = token.get(settings.SIMPLE_JWT["JTI_CLAIM"])
        user_id = token.get("user_id")
        self.redis_db.setex_jti(jti, time_to_live, user_id)

    def validate_and_blacklist_refresh_token(self, token):
        serializer = self.get_serializer(data={'token': token})

        if not serializer.is_valid():
            return Response({"message": "Refresh token is expired or is already blacklisted."},
                            status=status.HTTP_200_OK)

        refresh_token = serializer.validated_data['token']
        self.add_to_blacklist(refresh_token)

    def post(self, request):
        self.add_to_blacklist(request.data["access"])
        refresh_token = request.data.get("refresh", None)

        if not refresh_token:
            return Response({
                "error": "Invalid request",
                "message": "Refresh token was not provided, and the access token is already blacklisted."
            }, status=status.HTTP_400_BAD_REQUEST)

        self.validate_and_blacklist_refresh_token(refresh_token)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
