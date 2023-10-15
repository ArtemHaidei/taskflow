from django.urls import path

from users.views import (
    UserCreateView,
    UserRetriveView,
    UserUpdateView,
    UserDestroyView,
    UserListView,
    UserVerifyEmailView,
)

urlpatterns = [
    path(
        "users/",
        UserListView.as_view(),
        name="user-create",
    ),
    path(
        "create/",
        UserCreateView.as_view(),
        name="user-create",
    ),
    path(
        "user/<int:pk>/",
        UserRetriveView.as_view(),
        name="user-detail",
    ),
    path(
        "user/<int:pk>/update/",
        UserUpdateView.as_view(),
        name="user-update",
    ),
    path(
        "<int:pk>/delete/",
        UserDestroyView.as_view(),
        name="user-delete",
    ),
    path(
        "verify-email/",
        UserVerifyEmailView.as_view(),
        name="user-verify-email",
    ),
]
