from django.contrib import admin

from tasks.models import Category, Task

admin.site.register(Task)
admin.site.register(Category)
