from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.

class AccountCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('account_create')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass'
        }
        self.invalid_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': 'testpass'
        }
    
    def test_create_valid_user(self):
        response = self.client.post(self.url, data=self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)
    
    def test_create_existing_user(self):
        # First create a user
        self.client.post(self.url, data=self.valid_data, format='json')
        
        # Try to create a user with the same data as the first user
        response = self.client.post(self.url, data=self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_user(self):
        response = self.client.post(self.url, data=self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
