from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tasks.models import Category, Task
from tasks.serializers import (
    CategoryCreateSerializer,
    CategorySerializer,
    TaskCreateSerializer,
    TaskSerializer,
)


class TasksListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CategoriesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class CategoryCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
