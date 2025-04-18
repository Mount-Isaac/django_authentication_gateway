from django.contrib import admin

from .models import (
    CustomUser
)

# Register your models here.
def register_models(*models):
    [admin.site.register(model) for model in models]


register_models(
    CustomUser
)