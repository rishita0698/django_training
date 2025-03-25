# users/views.py

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer,PasswordChangeSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """create a new user in the system"""
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

class LoginView(TokenObtainPairView):
    """Login an existing user in the system"""
    permission_classes = (permissions.AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    """Creating a new access token from refresh token"""
    permission_classes = (permissions.AllowAny,)

class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    """Fetching & updating authorized user details"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get','put']

    def get_object(self):
        return self.request.user

class PasswordChangeView(generics.UpdateAPIView):
    """Updating the authroized user password """
    serializer_class = PasswordChangeSerializer
    model = CustomUser
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put']

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

