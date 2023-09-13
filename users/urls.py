from django.urls import path
from users.views import UserCreateView, UserVerifyEmailView, UserDeleteView, UserDetailView

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("user/<int:pk>/", UserDetailView.as_view(), name='user-detail'),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name='user-delete'),
    path("verify-email/", UserVerifyEmailView.as_view(), name='user-verify-email'),
]
