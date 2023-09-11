from rest_framework import generics
from login.serializers import AuthUserSerializer


class UserLoginView(generics.GenericAPIView):
    serializer_class = AuthUserSerializer
