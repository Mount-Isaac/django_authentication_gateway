from django.urls import path
from .views import (
    register_user,
    login_user,
    refresh_token,
    reset_password,
    reset_confirm_password,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register", register_user, name='register-user'),
    path("login", login_user, name='login-user'),
    path("refresh", refresh_token, name='refresh-user'),
    path("password-reset", reset_password, name='password-reset-request'),
    path("password-reset/confirm", reset_confirm_password, name='password-reset-confirm')
]