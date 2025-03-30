# users/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

User = get_user_model()

class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',  
            password='testpassword123',
            first_name='Test',
            last_name='User'
        )
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.refresh_url = reverse('auth-refresh-token')
        self.logout_url = reverse('auth-logout')
       
     
    def test_register_user(self):
        """test creating a user is successfull"""
        data = {
            "email": "test4@gmail.com",
            "first_name": "",
            "last_name": "",
            "password": "testpass123"
        }
        response = self.client.post(self.register_url, data, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User Registered Successfully")  
        self.assertEqual(User.objects.filter(email = data['email']).exists(), True)


    def test_register_without_optional_fields(self):
        "Test register without optional fields"

        data = {
            "email":"dummy@example.com",
            "password":"testpass123"
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email = data['email'])
        self.assertEqual(user.first_name , '')
        self.assertEqual(user.last_name , '')


    def test_register_invalid(self):
        "Test register without email"
        data = {
            "password":"testpass123"
        }

        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


    def test_login_success(self):
        """Test login a user"""
        response = self.client.post(self.login_url, {
            'email': self.user.email,  
            'password': 'testpassword123'  
        }, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure(self):
        """Test login a user"""
        response = self.client.post(self.login_url, {
            'email': self.user.email,  
            'password': 'testpassword'  
        }, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

     
    def test_token_refresh(self):
        """Test refresh token"""
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.refresh_url, {'refresh': str(refresh)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


    def test_token_refresh_invalid(self):
        """Test refresh token"""
        response = self.client.post(self.refresh_url, {'refresh': "Invalid toekn"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_logout_success(self):
        "Logout with valid refresh token"
        refresh = RefreshToken.for_user(self.user)
        print("refresh", refresh)
        data = {
            "refresh":str(refresh)
        }

        response = self.client.post(self.logout_url, data, format='json')
        print("response", response.json())
        self.assertEqual(response.status_code,  status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "successfully logged out")



    def test_logout_failure(self):
        "Logout with valid refresh token"
        data = {
            "refresh":"invalidetoken"
        }

        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  


class UserViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email = "user1@example.com",
            password = "testpass123",
            first_name = "Rishita",
            last_name = "khandelwal"
        )

        self.user2 = User.objects.create_user(
            email = "user2@example.com",
            password = "testpass123",
            first_name = "Rishi",
            last_name = "khandelwal"
        )

        self.access_token = str(AccessToken.for_user(self.user1))
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.access_token}')

        self.list_url = reverse('users-list')
        # self.retrieve_url = lambda pk:reverse('users-detail', args=['pk'])
        self.retrieve_url = reverse('users-detail', args=[self.user1.id])


    def test_list_users(self):
        "Test getting list of all the users"
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['email'], self.user1.email)
        self.assertEqual(response.data[1]['email'], self.user2.email)


    def test_retrieve_user_success(self):
        "Test reteriving a valid user by ID"
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user1.email)


    def test_retrieve_user_not_found(self):
        "Test reteriving a valid user by ID"
        self.retrieve_url = reverse('users-detail', args=[9999])
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'Error':"user not found"})

