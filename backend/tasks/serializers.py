import datetime

from django.utils.timesince import timesince
from rest_framework import serializers

from .models import Category, Task


# TODO: Add Validators for serializers
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        return Category.objects.create(user=user, **validated_data)


class TaskSerializer(serializers.ModelSerializer):
    deadline_at = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    @staticmethod
    def get_deadline_at(instance):
        deadline_date = instance.deadline_at
        now = datetime.datetime.now(tz=datetime.UTC)
        return timesince(now, deadline_date)


class TaskCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, required=False)

    class Meta:
        model = Task
        exclude = ("id", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        categories_data = validated_data.pop("categories")
        task = Task.objects.create(user=user, **validated_data)
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={"user": user},
            )
            task.categories.add(category)
        return task
