from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from emailsend.emailsend import EmailSender


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            msg = "The Email field must be set"
            raise ValueError(msg)

        email = self.normalize_email(email)

        if not password:
            msg = "The Password field must be set"
            raise ValueError(msg)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    temp_email = models.EmailField("temporary email", blank=True)
    name = models.CharField(max_length=30)
    phone_number = models.CharField("phone", max_length=30, blank=True)
    is_active = models.BooleanField("is_active", default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # noqa

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def send_verify_email(self):
        response = EmailSender().send_verify_email(self.pk)
        if response:
            print("Verification email for ", self.email)
            print(response)
        else:
            print("Error sending verification email for ", self.email)

    def send_reset_password_email(self):
        response = EmailSender().send_reset_password_email(self.pk)
        if response:
            print("Reset password email for ", self.email)
            print(response)
        else:
            print("Error sending reset password email for ", self.email)
