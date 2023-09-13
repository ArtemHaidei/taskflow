from django.urls import path
from users.views import (UserCreateView,
                         UserVerifyEmailView,
                         UserDeleteView,
                         UserDetailUpdateView)

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("user/<int:pk>/", UserDetailUpdateView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', UserDetailUpdateView.as_view(), name='user-update'),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name='user-delete'),
    path("verify-email/", UserVerifyEmailView.as_view(), name='user-verify-email'),
]
