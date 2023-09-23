from django.urls import path

from tasks.views import (
    CategoriesListView,
    CategoryCreateView,
    CategoryRetrieveUpdateDestroyView,
    TaskCreateView,
    TaskRetrieveUpdateDestroyView,
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
         TaskRetrieveUpdateDestroyView.as_view(),
         name="task-detail"),

    path("task/<int:pk>/update/",
         TaskRetrieveUpdateDestroyView.as_view(),
         name="task-update"),

    path("task/delete/<int:pk>/",
         TaskRetrieveUpdateDestroyView.as_view(),
         name="task-delete"),

    path("categories/",
         CategoriesListView.as_view(),
         name="category-list"),

    path("category/create/",
         CategoryCreateView.as_view(),
         name="category-create"),

    path("category/<int:pk>/",
         CategoryRetrieveUpdateDestroyView.as_view(),
         name="category-detail"),

    path("category/<int:pk>/update/",
         CategoryRetrieveUpdateDestroyView.as_view(),
         name="category-update"),

    path("category/delete/<int:pk>/",
         CategoryRetrieveUpdateDestroyView.as_view(),
         name="category-delete"),
]
