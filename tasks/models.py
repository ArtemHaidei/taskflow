from django.db import models
from users.models import User
from choiches import TaskPriority


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    if_description = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=TaskPriority.choices, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
