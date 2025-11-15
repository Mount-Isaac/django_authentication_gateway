from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from types import NoneType
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'is_active', 'password']

        extra_kwargs = {
            'password': { 'write_only': True },
            'is_active': { 'read_only': True }
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add custom user data
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    # confirm_password = serializers.CharField(write_only=True)

    # def validate(self, data):
    #     """
    #     Validate password & confirm password match 
    #     """

    #     if data.get("password") != data.get("confirm_password"):
    #         raise serializers.ValidationError({"confirm_password": "Passwords must match"})
        
    #     try:
    #         validate_password(data.get("new_password"))
    #     except Exception as e:
    #         return serializers.ValidationError({"new_password": list(e)})

    #     return data
