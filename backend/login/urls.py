from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from login.views import (UserLoginView,
                         UserLogoutView)


urlpatterns = [
    path("token/", UserLoginView.as_view(), name='token'),
    # path("token/destroy", UserLogoutView.as_view(), name='token-destroy'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]