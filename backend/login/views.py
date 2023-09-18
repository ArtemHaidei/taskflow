from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from login.serializers import LogoutTokenSerializer, AuthUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginView(TokenObtainPairView):
    serializer_class = AuthUserSerializer


class UserLogoutView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    # renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LogoutTokenSerializer

    @staticmethod
    def post(request):
        if request.user.is_anonymous:
            raise NotAuthenticated()

        request.data.get("token", request.auth.key)
        Token.objects.get(key=request.auth.key).delete()

        return Response(status=status.HTTP_200_OK)