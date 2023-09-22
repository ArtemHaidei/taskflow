from django.urls import path
from login.views import (CustomTokenRefreshView,
                         CustomTokenVerifyView,
                         UserLoginTokenPairView,
                         UserLogoutView)

urlpatterns = [
    path("token/", UserLoginTokenPairView.as_view(), name='token'),
    path("token/destroy", UserLogoutView.as_view(), name='token-destroy'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify')
]
