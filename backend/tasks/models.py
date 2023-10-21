from django.contrib.auth import get_user_model
from django.db import models

from choiches import TaskPriority, TaskStatus

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="category",
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="task",
    )
    title = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NONE,
    )

    category = models.ManyToManyField(Category, related_name="category")
    description = models.TextField(blank=True, default="")
    is_done = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20,
        choices=TaskPriority.choices,
        default=TaskPriority.LOW,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def set_if_different(self, key, value):
        current_value = getattr(self, key, None)
        if current_value != value:
            setattr(self, key, value)
            self.save()

    def add_category(self, user: User, categories: list) -> None:
        if len(categories) > 0:
            for category in categories:
                category_obj, _ = Category.objects.get_or_create(
                    name=category,
                    user=user,
                )
                self.category.add(category_obj)

    def remove_category(self, categories: list) -> None:
        if len(categories) > 0:
            for category in categories:
                category_obj = Category.objects.filter(name=category).first()
                if category_obj:
                    self.category.remove(category_obj)