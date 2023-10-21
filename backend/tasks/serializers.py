import datetime

from django.utils.timesince import timesince
from rest_framework import serializers

from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)
        extra_kwargs = {
            "name": {
                "validators": []
            }
        }

    @staticmethod
    def validate_name(value):
        if len(value) > 100:
            raise serializers.ValidationError("Category must be string")
        return value


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        return Category.objects.create(user=user, **validated_data)


class TaskSerializer(serializers.ModelSerializer):
    deadline_at = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        exclude = ("id", "user")

    @staticmethod
    def get_deadline_at(instance):
        deadline_date = instance.deadline_at
        now = datetime.datetime.now(tz=datetime.UTC)
        return timesince(now, deadline_date)


class TaskUpdateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        many=True, required=False, allow_empty=True
    )

    class Meta:
        model = Task
        exclude = ("id", "user", "created_at")

    def update(self, instance, validated_data):
        category_data = [item['name'] for item in validated_data.pop("category", [])]
        instance_category = list(instance.category.all())
        if category_data or instance_category:
            remove_categories = [category for category in instance_category if category not in category_data]
            instance.remove_category(categories=remove_categories)

            add_categories = [category for category in category_data if category not in instance_category]
            instance.add_category(user=self.context["request"].user, categories=add_categories)

        for key, value in validated_data.items():
            instance.set_if_different(key, value)

        return instance


class TaskCreateSerializer(serializers.ModelSerializer):
    category = CategoryCreateSerializer(many=True, required=False)

    class Meta:
        model = Task
        exclude = ("id", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        categories_data = validated_data.pop("category")
        task = Task(user=user, **validated_data)

        for category_data in categories_data:
            category = Category.objects.get_or_create(
                name=category_data["name"],
                user=user,
            )
            task.category.add(category)

        task.save()
        return task
