from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)


    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username.capitalize()
    
    @classmethod
    def get_by_natural_key(self, username):
        return self.objects.get(
            models.Q(username=username) | models.Q(email=username)
        )