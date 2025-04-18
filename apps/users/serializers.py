from .models import CustomUser
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer)
    class Meta:
        model = CustomUser
        fields = "__all__"