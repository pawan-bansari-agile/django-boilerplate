from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, extend_schema_view
User = get_user_model()

class SignupView(APIView):
    @extend_schema(
        summary="Sign up a new user",
        description="Creates a new user with the provided details.",
        request=SignupSerializer,
        responses={
            201: {"description": "User created successfully"},
            400: {"description": "Validation error"}
        },
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestView(APIView):
    @extend_schema(
        summary="Test API endpoint",
        description="Returns a welcome message.",
        responses={200: {"description": "Success"}}
    )
    def get(self, request):
        data = {"message": "Welcome to the API!"}
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Simulate an error for testing",
        description="Throws a simulated error for testing exception handling.",
        responses={500: {"description": "Internal server error"}}
    )
    def post(self, request):
        # Simulate an error
        # raise ValueError("This is a simulated error for testing.")
        return Response({'error': 'This is a simulated error for testing.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgetPasswordView(APIView):
    @extend_schema(
        summary="Request a password reset",
        description="Requests a password reset by providing an email.",
        request=None,
        responses={
            200: {"description": "Password reset link sent to your email."},
            400: {"description": "Email is required."},
            404: {"description": "User with this email does not exist."}
        }
    )
    def post(self, request):
        email = request.data.get('email')
        print('email', email)
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            # print('user', user)
            # Simulated response (No email functionality implemented yet)
            return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    @extend_schema(
        summary="Reset a user's password",
        description="Resets the password using email and new password details.",
        request=None,
        responses={
            200: {"description": "Password reset successfully."},
            400: {"description": "Validation error or passwords do not match."},
            404: {"description": "User with this email does not exist."}
        }
    )
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not email or not new_password or not confirm_password:
            return Response({'error': 'All fields (email, new_password, confirm_password) are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
