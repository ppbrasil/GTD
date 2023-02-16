from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.models import Task


class TaskCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='taskcreateuser', password='testpass123', email='taskcreateuser@example.com')

    def test_create_valid_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task_create')
        data = {
            'name': 'Test Task 1',
            'focus': True,
            'done': False,
            'waiting_for': None,
            'due_date': None,
            'reminder': None,
            'readiness': 'inbox',
            'notes': 'This is a test task'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.name, 'Test Task 1')
        self.assertTrue(task.focus)
        self.assertFalse(task.done)
        self.assertIsNone(task.waiting_for)
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.reminder)
        self.assertEqual(task.readiness, 'inbox')
        self.assertEqual(task.notes, 'This is a test task')

    def test_create_task_with_name_only(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task_create')
        data = {
            'name': 'Task with name only'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Task with name only')
        self.assertEqual(task.focus, False)
        self.assertEqual(task.done, False)
        self.assertEqual(task.waiting_for, None)
        self.assertEqual(task.due_date, None)
        self.assertEqual(task.reminder, None)
        self.assertEqual(task.readiness, 'inbox')
        self.assertEqual(task.notes, None)

    def test_create_invalid_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('task_create')
        data = {
            'name': '',
            'focus': True,
            'done': False,
            'waiting_for': None,
            'due_date': None,
            'reminder': None,
            'readiness': 'inbox',
            'notes': 'This is a test task'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')

    def test_authentication_required(self):
        url = reverse('task_create')
        data = {
            'name': 'Test Task 1',
            'focus': True,
            'done': False,
            'waiting_for': None,
            'due_date': None,
            'reminder': None,
            'readiness': 'inbox',
            'notes': 'This is a test task'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 0)
    