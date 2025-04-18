from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
# Create your views here.

class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({"message": "user registered successfully", "user":user_serializer.data}, status=status.HTTP_201_CREATED)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # yet to log 
            return Response(status=status.HTTP_400_BAD_REQUEST)



class PasswordResetView(APIView):
    pass


register_user = RegisterUserView.as_view()
reset_password = PasswordResetView.as_view()