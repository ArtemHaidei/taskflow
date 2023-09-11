import secrets

from users.models import User
from django.db import models


class MagicLinkToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Magic Link Token for {self.user.email}"

    @classmethod
    def create_token(cls, user):
        token = cls.generate_token()
        instance = cls.objects.create(token=token, user=user)
        return instance

    @staticmethod
    def generate_token(nbytes=32):
        return secrets.token_urlsafe(nbytes)
