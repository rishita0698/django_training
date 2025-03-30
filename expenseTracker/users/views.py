# users/views.py

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer,LoginSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AuthViewSet(viewsets.ViewSet):
    """View for User Auth"""
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
            request_body=CustomUserSerializer,
            responses={200:CustomUserSerializer()}
    )
    @action(detail = False, methods = ['post'])
    def register(self, request):
        """Create a new user/user signup"""
        serializer = CustomUserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
            request_body=LoginSerializer,
            responses={200:CustomUserSerializer()}
    )
    @action(detail = False, methods=['post'])
    def login(self, request):
        """Login the existing user"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            custom_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'id':user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            return Response(custom_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
            request_body=openapi.Schema(
                type = openapi.TYPE_OBJECT,
                properties = {
                    'refresh':openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token")
                },
                required = ['refresh']
            ),
            responses={200:"New access token",400:"Invalid refresh token"}
    )
    @action(detail = False, methods = ['post'])
    def refresh_token(self, request):
        """Create new access token from refresh token"""
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"error":"Refresh token is Required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            return Response({"access":str(token)}, status = status.HTTP_200_OK)
        except Exception:
            return Response({"error":"Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type = openapi.TYPE_OBJECT,
                properties = {
                    'refresh':openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token")
                },
                required = ['refresh']
            ),
            responses={200:"Logout successful",400:"Invalid token"}
    )
    @action(detail = False, methods = ['post'])
    def logout(self, request):
        """User logout view"""
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"successfully logged out"}, status = status.HTTP_200_OK)
        except Exception:
            return Response({"error":"Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        


class UserViewSet(viewsets.ViewSet):
    """View for the user details"""
    def list(self, request):
        """List all the users"""
        users = CustomUser.objects.all()
        serialize = CustomUserSerializer(users, many = True)
        return Response(serialize.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        """Get Existing user details"""
        try:
            user = CustomUser.objects.get(pk=pk)
            serialize = CustomUserSerializer(user)
            return Response(serialize.data, status = status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"Error":"user not found"}, status=status.HTTP_404_NOT_FOUND)