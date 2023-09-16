from django.db import models
from choiches import TaskPriority, TaskStatus

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.NONE)
    category = models.ManyToManyField(Category, related_name='categories')
    description = models.TextField(blank=True, null=True)
    if_description = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=TaskPriority.choices, default='Low')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
