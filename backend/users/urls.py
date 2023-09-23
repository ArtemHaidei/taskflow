from django.urls import path

from users.views import (
    UserCreateView,
    UserDetailUpdateDeleteView,
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
        UserDetailUpdateDeleteView.as_view(),
        name="user-detail",
    ),
    path(
        "user/<int:pk>/update/",
        UserDetailUpdateDeleteView.as_view(),
        name="user-update",
    ),
    path(
        "delete/<int:pk>/",
        UserDetailUpdateDeleteView.as_view(),
        name="user-delete",
    ),
    path(
        "verify-email/",
        UserVerifyEmailView.as_view(),
        name="user-verify-email",
    ),
]
