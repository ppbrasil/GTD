from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token

User = get_user_model()

class AccountCreateTestCase(APITestCase):
    def test_create_valid_user(self):
        url = reverse('account_create')
        data = {
            'username': 'valid_testuser',
            'password': 'testpass123',
            'email': 'testvaliduser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=data['username']).exists())

    def test_create_existing_user(self):
        User.objects.create_user(username='invalid_testuser', password='testpass123', email='testinvaliduser@example.com')
        url = reverse('account_create')
        data = {
            'username': 'invalid_testuser',
            'password': 'testpass123',
            'email': 'testinvaliduser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')

class TokenGenerateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testtokenuser', password='testpass123', email='testtokenuser@example.com')

    def test_token_generation(self):
        url = reverse('obtain-token')
        data = {
            'username': 'testtokenuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
    
    def test_token_generation_for_non_existing_user(self):
        url = reverse('obtain-token')
        data = {
            'username': 'non_existing_user',
            'password': 'non_existing_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('non_field_errors' in response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Unable to log in with provided credentials.')

class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_logout', password='testpass123')
        self.token = Token.objects.create(user=self.user)

    def test_logout_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_logout_non_authenticated_user(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(key=self.token.key).exists())
