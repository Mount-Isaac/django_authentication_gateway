from django.urls import path
from .views import (
    register_user,
    reset_password
)

urlpatterns = [
    path("register/", register_user, name='register-user'),
    path("password-reset/", reset_password, name='password-reset-request'),
    path("password-reset/confirm/", reset_password, name='password-reset-confirm')
]