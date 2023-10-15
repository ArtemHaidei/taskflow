from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from users.serializers import (
    CreateUserSerializer,
    UserEmailPasswordSerializer,
    UserSerializer,
)
from users.utils import decode_jwt_token, get_user_by_email

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class UserListView(generics.ListAPIView):
    permission_classes = (IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetriveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserVerifyEmailView(APIView):
    @staticmethod
    def get(request):
        jwt_token = request.GET.get("token")
        decoded_data = decode_jwt_token(jwt_token).get("decoded_data", None)

        if not decoded_data:
            return Response(
                data=decoded_data["detail"],
                status=decoded_data["status"],
            )

        user = get_user_by_email(decoded_data.get("email"))
        if user:
            user.is_active = True
            user.save()
            return Response(
                data={"detail": "Email is confirmed!"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"detail": "User does not exist!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# TODO: Implement UserResetPasswordView # noqa: FIX002
class UserResetPasswordView(generics.GenericAPIView):
    serializer_class = UserEmailPasswordSerializer

    @staticmethod
    def post(request):
        jwt_token = request.GET.get("token")
        decoded_data = decode_jwt_token(jwt_token).get("decoded_data", None)

        if not decoded_data:
            return Response(
                data=decoded_data["detail"],
                status=decoded_data["status"],
            )

        user = get_user_by_email(decoded_data.get("email"))
        if user:
            user.set_password(decoded_data.get("password"))
            user.save()
            return Response(
                data={"detail": "Password is reset!"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"detail": "User does not exist!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
