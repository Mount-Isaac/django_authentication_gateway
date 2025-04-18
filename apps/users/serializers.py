from .models import CustomUser
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'is_active', 'password']

        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
