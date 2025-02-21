from django.db import models

# Create your models here.

class Token(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)