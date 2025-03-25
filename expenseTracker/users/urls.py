# users/urls.py

from django.urls import path
from .views import RegisterView, UserDetailUpdateView, PasswordChangeView, LoginView, CustomTokenRefreshView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Customizing the tags for the endpoints
register_view = swagger_auto_schema(
    method='post',
    tags=['Users'],
    operation_description="Register a new user",
)(RegisterView.as_view())

login_view = swagger_auto_schema(
    method='post',
    tags=['Users'],
    operation_description="Log in a user and obtain a JWT token",
)(LoginView.as_view())

token_refresh_view = swagger_auto_schema(
    method='post',
    tags=['Users'],
    operation_description="Refresh the JWT token",
)(CustomTokenRefreshView.as_view())

update_user_password_view = swagger_auto_schema(
    method='put',
    tags=['Users'],
    operation_description="Update/Change Password",
)(PasswordChangeView.as_view())

user_detail_view = swagger_auto_schema(
    methods=['get','put'],
    tags=['Users'],
    operation_description="Get/Update User Detail",
)(UserDetailUpdateView.as_view())


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('token/refresh/', token_refresh_view, name='token_refresh'),
    path('user/', user_detail_view, name='user_detail'),
    path('user/change-password/', update_user_password_view, name='password_change'),  # Add the password change endpoint
]


