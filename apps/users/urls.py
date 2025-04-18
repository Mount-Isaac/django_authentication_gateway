from django.urls import path
from .views import register_user

urlpatterns = [
    path("register/", register_user, name='register-user')
]