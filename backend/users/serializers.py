from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from tasks.serializers import TaskSerializer, CategorySerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        # exclude = ('password', 'is_active', 'is_staff', 'is_superuser')
        # exclude = ('password',)
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("name", 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])
        user.name = validated_data['name']
        user.save()
        return user


class UserEmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

