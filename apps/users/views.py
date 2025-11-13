from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    UserSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer
)
from .models import (
    CustomUser
)


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



class PasswordResetRequestView(APIView):
    """
    Requests a password link via email
    """
    def post(sekf, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
                print(reset_link)
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return Response({
                    "success": "Password reset email has been sent."
                }, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                # security checkpoint 
                # return success even if user does not exist
                return Response({
                    "success": "Password reset email has been sent."
                }, status=status.HTTP_200_OK)
            except Exception as e:
                # log error 
                print(str(e))
                return Response({
                    "error": "Failed to process password reset"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









# convert class based view to func_based views
register_user = RegisterUserView.as_view()
reset_password = PasswordResetRequestView.as_view()