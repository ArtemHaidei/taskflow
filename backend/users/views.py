from rest_framework import generics, status
from rest_framework.response import Response

from users.serializers import CreateUserSerializer, UserSerializer, UserEmailPasswordSerializer
from users.utils import get_user_by_email, decode_jwt_token
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# TODO: Implement UserVerifyEmailView and UserResetPasswordView
class UserVerifyEmailView(generics.GenericAPIView):
    @staticmethod
    def get(request):
        jwt_token = request.GET.get("token")
        decoded_data = decode_jwt_token(jwt_token).get("decoded_data", None)

        if not decoded_data:
            return Response(data=decoded_data["detail"], status=decoded_data["status"])

        user = get_user_by_email(decoded_data.get("email"))
        if user:
            user.is_active = True
            user.save()
            return Response({'detail': 'Email is confirmed!'}, status=status.HTTP_200_OK)

        return Response({'detail': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(generics.GenericAPIView):
    serializer_class = UserEmailPasswordSerializer

    @staticmethod
    def post(request):
        jwt_token = request.GET.get("token")
        decoded_data = decode_jwt_token(jwt_token).get("decoded_data", None)

        if not decoded_data:
            return Response(data=decoded_data["detail"], status=decoded_data["status"])

        user = get_user_by_email(decoded_data.get("email"))
        if user:
            user.set_password(decoded_data.get("password"))
            user.save()
            return Response({'detail': 'Password is reset!'}, status=status.HTTP_200_OK)

        return Response({'detail': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
