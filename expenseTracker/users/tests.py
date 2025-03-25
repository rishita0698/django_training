# users/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        self.me_url = reverse('user_detail')
        self.update_url = reverse('user_detail')
        self.password_change_url = reverse('password_change')  
        self.user_data = {
            'email': 'newuser@example.com',  
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = CustomUser.objects.create_user(
            email='existinguser@example.com',  
            password='testpassword123',
            first_name='Existing',
            last_name='User'
        )

    def test_register_user(self):
        """test creating a user is successfull"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)  
        self.assertEqual(CustomUser.objects.get(email=self.user_data['email']).email, self.user_data['email'])

    def test_login_user(self):
        """Test login a user"""
        response = self.client.post(self.login_url, {
            'email': self.user.email,  
            'password': 'testpassword123'  
        }, format='json')
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


    def test_token_refresh(self):
        """Test refresh token"""
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.refresh_url, {'refresh': str(refresh)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_user_details(self):
        """Test for retreiving user details"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_get_user_details_unauthenticated(self):
        """Test for unauthorized user access"""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_details(self):
        """Test for update user profile"""
        self.client.force_authenticate(user=self.user)
        update_data = {
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.put(self.update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data['first_name'])
        self.assertEqual(self.user.last_name, update_data['last_name'])

    def test_change_password(self):
        """Test for change password"""
        self.client.force_authenticate(user=self.user)
        password_data = {
            'old_password': 'testpassword123',
            'new_password': 'newpassword123'
        }
        response = self.client.put(self.password_change_url, password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(password_data['new_password']))
