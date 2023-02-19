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


class TaskUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='taskupdateuser', password='testpass123', email='taskupdateuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            user=self.user,
            is_active = True,
            name='Test Task 1',
            focus=True,
            done=False,
            due_date=None,
            reminder=None,
            readiness='inbox',
            notes='This is a test task'
        )

    def test_update_valid_task(self):
        url = reverse('task_update', kwargs={'pk': self.task.id})
        data = {
            'name': 'Updated Test Task',
            'focus': False,
            'done': True,
            'due_date': '2023-03-15',
            'reminder': '2023-03-14T14:30:00Z',
            'readiness': 'anytime',
            'notes': 'This is an updated test task'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.name, 'Updated Test Task')
        self.assertFalse(task.focus)
        self.assertTrue(task.done)
        self.assertEqual(str(task.due_date), '2023-03-15')
        self.assertEqual(str(task.reminder), '2023-03-14 14:30:00+00:00')
        self.assertEqual(task.readiness, 'anytime')
        self.assertEqual(task.notes, 'This is an updated test task')

    def test_update_invalid_task_id(self):
        url = reverse('task_update', kwargs={'pk': self.task.id + 1})
        data = {
            'name': 'Updated Test Task',
            'focus': False,
            'done': True,
            'due_date': '2023-03-15',
            'reminder': '2023-03-14T14:30:00Z',
            'readiness': 'next',
            'notes': 'This is an updated test task'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_deactivated_task(self):
        self.task.is_active = False
        self.task.save()
        url = reverse('task_update', kwargs={'pk': self.task.id})
        data = {
            'name': 'Updated Test Task',
            'focus': False,
            'done': True,
            'due_date': '2023-03-15',
            'reminder': '2023-03-14T14:30:00Z',
            'readiness': 'waiting',
            'notes': 'This is an updated test task'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.name, 'Test Task 1')
        self.assertTrue(task.focus)
        self.assertFalse(task.done)
        self.assertEqual(task.due_date, None)
        self.assertEqual(task.reminder, None)
        self.assertEqual(task.readiness, 'inbox')
        self.assertEqual(task.notes, 'This is a test task')


class TaskToggleFocusAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasktogglefocususer1', 
            password='testpass123', 
            email='tasktogglefocususer1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasktogglefocususer2', 
            password='testpass123', 
            email='tasktogglefocususer2@example.com'
            )
        self.task = Task.objects.create(
            user=self.user1,
            name='Test Task',
            focus=False,
            done=False,
            readiness='inbox',
        )
        print (self.task.id)
        print(self.task.focus)

    def test_toggle_focus_valid_task(self):
        self.client.force_authenticate(user=self.user1)
        print (self.task.id)
        url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        print(f'task.focus = {task.focus}')
        self.assertTrue(task.focus)

    # def test_toggle_focus_invalid_task_id(self):
    #     self.client.force_authenticate(user=self.user1)
    #     url = reverse('task_toggle_focus', kwargs={'pk': self.task.id + 1})
    #     response = self.client.patch(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_toggle_focus_unauthenticated_user(self):
    #     url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
    #     response = self.client.patch(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_toggle_focus_other_user_task(self):
    #     self.client.force_authenticate(user=self.user2)
    #     url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
    #     response = self.client.patch(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_toggle_focus_deactivated_task(self):
    #     self.client.force_authenticate(user=self.user1)
    #     self.task.is_active = False
    #     self.task.save()
    #     url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
    #     response = self.client.patch(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     task = Task.objects.get(id=self.task.id)
    #     self.assertFalse(task.focus)
