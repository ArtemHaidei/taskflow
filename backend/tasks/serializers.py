from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers
from .models import Task, Category


# TODO: Validators
class CategorySerializer(serializers.ModelSerializer):
    deadline_at = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    @staticmethod
    def get_deadline_at(instance):
        deadline_date = instance.deadline_at
        now = datetime.now()
        time_delta = timesince(now, deadline_date)
        return time_delta


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', 'user')


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Task
        exclude = ('id', 'user')

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     categories_data = validated_data.pop('categories')
    #     task = Task.objects.create(user=user, **validated_data)
    #     for category_data in categories_data:
    #         category, created = Category.objects.get_or_create(name=category_data['name'], defaults={'user': user})
    #         task.categories.add(category)
    #     return task
