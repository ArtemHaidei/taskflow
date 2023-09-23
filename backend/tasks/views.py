from rest_framework import generics

from tasks.models import Category, Task
from tasks.serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
    TaskCreateSerializer,
    TaskSerializer,
)


class TasksListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CategoriesListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
