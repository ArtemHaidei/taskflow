from django.urls import path

from tasks.views import (
    CategoriesListView,
    CategoryCreateView,
    CategoryRetrieveView,
    CategoryUpdateView,
    CategoryDestroyView,
    TaskCreateView,
    TaskRetrieveView,
    TaskUpdateView,
    TaskDestroyView,
    TasksListView,
)

urlpatterns = [
    path("tasks/",
         TasksListView.as_view(),
         name="tasks-list"),

    path("task/create/",
         TaskCreateView.as_view(),
         name="task-create"),

    path("task/<int:pk>/",
         TaskRetrieveView.as_view(),
         name="task-detail"),

    path("task/<int:pk>/update/",
         TaskUpdateView.as_view(),
         name="task-update"),

    path("task/<int:pk>/delete/",
         TaskDestroyView.as_view(),
         name="task-delete"),

    path("categories/",
         CategoriesListView.as_view(),
         name="category-list"),

    path("category/create/",
         CategoryCreateView.as_view(),
         name="category-create"),

    path("category/<int:pk>/",
         CategoryRetrieveView.as_view(),
         name="category-detail"),

    path("category/<int:pk>/update/",
         CategoryUpdateView.as_view(),
         name="category-update"),

    path("category/<int:pk>/delete/",
         CategoryDestroyView.as_view(),
         name="category-delete"),
]
