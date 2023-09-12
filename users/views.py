from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ParseError

from users.serializers import CreateUserSerializer
from users.utils import get_user_by_email, decode_jwt_token
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise ParseError("Invalid data")
        serializer.save()
        return Response(data={"detail": "User created successfully",
                              "user": serializer.data},
                        status=status.HTTP_201_CREATED)


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
