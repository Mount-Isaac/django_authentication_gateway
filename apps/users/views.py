from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer
)
from .models import (
    CustomUser
)
from apps.helpers import (
    format_response,
    flatten_errors
)

# Create your views here.
class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    format_response(
                        success=True,
                        message="user registered successfully",
                        data=user_serializer.data,
                        request_id=request.id,
                    ), status=status.HTTP_201_CREATED
                )
            return Response(
                format_response(
                    success=False,
                    message='Failed to create user.',
                    request_id=request.id,
                    error=flatten_errors(user_serializer.errors)
                ),status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # print(e)
            return Response(
                format_response(
                    success=False,
                    message='Failed to create user.',
                    request_id=request.id,
                    error=[str(e)]
                ),status=status.HTTP_400_BAD_REQUEST
            )


class LoginUserView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        try:
            login_serializer = MyTokenObtainPairSerializer(data=request.data)
            if not login_serializer.is_valid():
                return Response(
                    format_response(
                        success=False,
                        message='Login failed. Incorrect username/password.',
                        request_id=request.id,
                        error=flatten_errors(login_serializer.errors)
                    ),status=status.HTTP_400_BAD_REQUEST
                )
            
            user = login_serializer.user

            refresh_token = RefreshToken.for_user(user)
            refresh_token['email'] = user.email
            refresh_token['first_name'] = user.first_name
            refresh_token['last_name'] = user.last_name

            data = {
                "access": str(refresh_token.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }
            response = Response(
                format_response(
                    success=True,
                    message="Login successful",
                    data=data,
                    request_id=request.id,
                ), status=status.HTTP_201_CREATED
            )
            response.set_cookie(
                key='refresh',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='Strict',
                path='/api/auth/refresh',
            )
            return response
        except Exception as e:
            # print(e)
            return Response(
                format_response(
                    success=False,
                    message='Login failed',
                    request_id=request.id,
                    error=[str(e)]
                ),status=status.HTTP_400_BAD_REQUEST
            )


class RefreshTokenView(TokenRefreshView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh")
            if not refresh_token:
                return Response(
                    format_response(
                        success=False,
                        message='No refresh token found.',
                        request_id=request.id,
                        error=["Refresh token: No refresh token found in cookie."]
                    ),status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.get_serializer(data={ "refresh": refresh_token })
            if not serializer.is_valid():
                return Response(
                    format_response(
                        success=False,
                        message='Request failed. Try again.',
                        request_id=request.id,
                        error=flatten_errors(serializer.errors)
                    ),status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                format_response(
                    success=True,
                    message="Request successful",
                    data={ "access": serializer.validated_data.get("access", "") },
                    request_id=request.id,
                ), status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # print(e)
            return Response(
                format_response(
                    success=False,
                    message='Failed to refresh token. Try again.',
                    request_id=request.id,
                    error=[str(e)]
                ),status=status.HTTP_400_BAD_REQUEST
            )
        

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
                # print(user.id, 'user found')
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
                # print(reset_link)
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_link}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                return Response(
                    format_response(
                        success=True,
                        message="Password reset email sent.",
                        request_id=request.id
                    ), status=status.HTTP_200_OK
                )
            except CustomUser.DoesNotExist:
                return Response(
                    format_response(
                        success=False,
                        message="User with this email does not exist.",
                        request_id=request.id,
                        error=['Email: user does not exist.']
                    ), status=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                # log error 
                # print(str(e))
                return Response(
                    format_response(
                        success=False,
                        message='Requst failed. Try again later.',
                        request_id=request.id,
                        error=[str(e)]
                    ),status=status.HTTP_400_BAD_REQUEST
                )
        

class PasswordResetConfirmView(APIView):
    """
    Requests a password link via email
    """
    def post(self, request, *args, **kwargs):
        try:
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    format_response(
                        success=False,
                        message='Invalid password reset request.',
                        request_id=request.id,
                        error=flatten_errors(serializer.errors),
                    ),status=status.HTTP_400_BAD_REQUEST
                )
            
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                user = CustomUser.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
                if default_token_generator.check_token(user, token):
                    # print(user.email)
                    user.set_password(new_password)
                    user.save()

                    return Response(
                        format_response(
                            success=True,
                            message="Password has been reset successfully.",
                            request_id=request.id
                        ), status=status.HTTP_200_OK
                    )
                
                return Response(
                    format_response(
                        success=False,
                        message="Invalid or expired token.",
                        request_id=request.id
                    ), status=status.HTTP_400_BAD_REQUEST
                )
            except CustomUser.DoesNotExist:
                return Response(
                    format_response(
                        success=False,
                        message="User with this email does not exist.",
                        request_id=request.id,
                        error=['Email: user does not exist.']
                    ), status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            # log error 
            # # print(str(e))
            return Response(
                format_response(
                    success=False,
                    message='Invalid password reset request.',
                    request_id=request.id,
                    error=[str(e)]
                ),status=status.HTTP_400_BAD_REQUEST
            )



# convert class based view to func_based views
register_user = RegisterUserView.as_view()
login_user = LoginUserView.as_view()
refresh_token = RefreshTokenView.as_view()
reset_password = PasswordResetRequestView.as_view()
reset_confirm_password = PasswordResetConfirmView.as_view()