from django.urls import path
from .views import (
    register_user,
    reset_password
)

urlpatterns = [
    path("register/", register_user, name='register-user'),
    path("reset/password/", reset_password, name='reset-password')
]