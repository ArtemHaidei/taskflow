import jwt

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.conf import settings


def get_user_by_email(email):
    from users.models import User
    try:
        user = User.objects.get(email=email)
        return user
    except ObjectDoesNotExist:
        return


def get_user_by_pk(pk):
    from users.models import User
    try:
        user = User.objects.get(pk=pk)
        return user
    except ObjectDoesNotExist:
        return


def decode_jwt_token(jwt_token):
    try:
        decoded_data = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        return {'decoded_data': decoded_data}

    except jwt.ExpiredSignatureError:
        return {'detail': 'Link is expired!', 'status': status.HTTP_400_BAD_REQUEST}
    except jwt.DecodeError:
        return {'detail': 'Link is not active!', 'status': status.HTTP_400_BAD_REQUEST}
    except jwt.InvalidTokenError:
        return {'detail': 'Invalid link!', 'status': status.HTTP_400_BAD_REQUEST}


