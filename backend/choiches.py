from django.db import models


class TaskPriority(models.TextChoices):
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"
    LOW = "low", "Low"


class TaskStatus(models.TextChoices):
    NONE = "none", "None"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELED = "canceled", "Canceled"
