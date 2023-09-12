from django.urls import path
from users.views import UserCreateView, UserVerifyEmailView


urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
    path("verify-email/", UserVerifyEmailView.as_view(), name='user-verify-email'),
]