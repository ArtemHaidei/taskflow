from rest_framework import generics, status
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ParseError

from users.serializers import CreateUserSerializer, UserDetailSerializer
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


class UserDetailUpdateView(UpdateModelMixin, RetrieveModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user)
        return Response(data={'detail': f'User {user} detail.',
                              'user': serializer.data},
                        status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)
        if not serializer.is_valid():
            raise ParseError("Invalid data")
        serializer.save()
        return Response(data={'detail': f'User {user} update successful!',
                              'user': serializer.data},
                        status=status.HTTP_200_OK)


class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        email = user.email
        deleted, _ = user.delete()
        if not deleted:
            raise ParseError(f"Account {email} was not deleted")
        return Response({'detail': f'Account {email} was deleted!'},
                        status=status.HTTP_204_NO_CONTENT)


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
