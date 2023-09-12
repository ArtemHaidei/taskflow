from rest_framework import generics, parsers, renderers, status
from django.contrib.auth.hashers import check_password
from login.serializers import AuthUserSerializer
from users.serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed, ParseError, PermissionDenied
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotAuthenticated
from login.serializers import LogoutTokenSerializer


class UserLoginView(generics.GenericAPIView):
    serializer_class = AuthUserSerializer

    def validate(self, data):
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            raise ParseError("Invalid data")
        return self.get_user(serializer.validated_data["email"])

    @staticmethod
    def check_password(password, account):
        if not check_password(password, account.password):
            raise AuthenticationFailed()

    @staticmethod
    def check_is_active(account):
        if account.is_active is False:
            raise PermissionDenied("User account is not activate.")

    @staticmethod
    def get_user(email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as error:
            raise AuthenticationFailed() from error
        return user

    def post(self, request):
        user = self.validate(request.data)
        self.check_password(request.data.get("password"), user)
        self.check_is_active(user)
        token, created = Token.objects.get_or_create(user=user)

        return Response(status=status.HTTP_200_OK,
                        data={
                            "user": UserSerializer(instance=user, many=False).data,
                            "token": token.key
                        })


class UserLogoutView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LogoutTokenSerializer

    def post(self, request):
        if request.user.is_anonymous:
            raise NotAuthenticated()

        request.data.get("token", request.auth.key)
        Token.objects.get(key=request.auth.key).delete()

        return Response(status=status.HTTP_200_OK)
