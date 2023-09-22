from django.urls import path
from login.views import (CustomTokenAccessRefreshView,
                         CustomTokenVerifyView,
                         UserLoginTokenPairView,
                         UserLogoutView)

urlpatterns = [
    path("token/", UserLoginTokenPairView.as_view(), name='token'),
    path("token/destroy/", UserLogoutView.as_view(), name='token-destroy'),
    path('token/refresh/', CustomTokenAccessRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token-verify')
]
