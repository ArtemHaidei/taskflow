from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# from django.utils import timezone


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        """Creates and saves a User with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)

        if not password:
            raise ValueError("The Password field must be set")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault("user_type", "admin")
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_email_confirmed", True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    temp_email = models.EmailField("temporary email", blank=True)
    nickname = models.CharField(max_length=30, unique=True, null=True)
    name = models.CharField(max_length=30)
    phone_number = models.CharField("phone", max_length=30, blank=True)
    is_active = models.BooleanField('is_active', default=False)
    is_staff = models.BooleanField('is_staff', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email
