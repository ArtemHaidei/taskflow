from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from login.serializers import (
    AuthUserTokenPairSerializer,
    TokenAccessRefreshSerializer,
    TokenLogoutSerializer,
    TokenVerifySerializer,
)

User = get_user_model()


class CustomTokenAccessRefreshView(TokenRefreshView):
    serializer_class = TokenAccessRefreshSerializer


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = TokenVerifySerializer


class UserLoginTokenPairView(TokenObtainPairView):
    serializer_class = AuthUserTokenPairSerializer


class UserLogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenLogoutSerializer

    def post(self, request):
        access_token = request.META.get("HTTP_AUTHORIZATION", "").split(" ")[1]
        refresh_token = request.data.get("refresh", None)
        serializer = self.get_serializer(
            data={"access": access_token, "refresh": refresh_token},
        )
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
