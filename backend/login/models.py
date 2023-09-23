import secrets

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MagicLinkToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Magic Link Token for {self.user.email}"  # type: ignore

    @classmethod
    def create_token(cls, user):
        token = cls.generate_token()
        return cls.objects.create(token=token, user=user)

    @staticmethod
    def generate_token(nbytes=32):
        return secrets.token_urlsafe(nbytes)
