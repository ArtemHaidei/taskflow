from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('id', 'password')


class UserEmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("name", 'email', 'password')

    def save(self, **kwargs):
        user = User.objects.create_user(
            name=self.validated_data['name'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        user.send_verify_email()
