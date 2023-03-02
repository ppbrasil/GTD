import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.models import Task, Tag

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

    def test_create_task_with_tags(self):
        self.client.force_authenticate(user=self.user)
        # Create a task with tags
        url = reverse('task_create')
        data = {
            'name': 'Test task',
            'tags': [{'name': 'tag1'}, {'name': 'tag2'}]
        }
        print(data)
        response = self.client.post(url, data, format='json')
        print('Request data:', json.dumps(data))
        print('Response data:', response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the task and tags have been created
        task = Task.objects.get(name='Test task')
        print(task.tags.all())
        self.assertEqual(task.name, 'Test task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.tags.count(), 2)
        self.assertTrue(task.tags.filter(name='tag1').exists())
        self.assertTrue(task.tags.filter(name='tag2').exists())
        
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

    def test_add_new_tag_to_task(self):
        # Add existing tag to task's tag list
        existing_tag_data = {'name': 'Tag 1', 'user': self.user.id}
        data = {'tags': [existing_tag_data]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 1)
        self.assertIn(existing_tag_data['name'], [tag.name for tag in task.tags.all()])

        # Add new tag to task's tag list
        new_tag_data = {'name': 'New Tag', 'user': self.user.id}
        data = {'tags': [existing_tag_data, new_tag_data]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 2)
        self.assertIn(existing_tag_data['name'], [tag.name for tag in task.tags.all()])
        self.assertIn(new_tag_data['name'], [tag.name for tag in task.tags.all()])

    def test_add_existing_tag_to_task(self):
        # Create an existing tag
        existing_tag_name = 'Existing Tag'
        existing_tag = Tag.objects.create(name=existing_tag_name, user=self.user)
        
        # Add existing tag to task's tag list
        data = {'tags': [{'name': existing_tag_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 1)
        self.assertIn(existing_tag, task.tags.all())

    def test_create_new_tag_while_trying_to_add_tag_with_same_name_but_from_different_user_to_task(self):
        another_user=User.objects.create()

        # Create an existing tag with the same name but a different user
        existing_tag_name = 'Tag from other user'
        existing_tag = Tag.objects.create(name=existing_tag_name, user=another_user)
        
        # Add existing tag to task's tag list
        data = {'tags': [{'name': existing_tag_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 1)
        self.assertNotIn(existing_tag, task.tags.all())
        self.assertIn(existing_tag_name, [tag.name for tag in task.tags.all()])

    def test_remove_all_tags_from_task(self):
        # Add some tags to the task
        tag1 = Tag.objects.create(name='Tag 1', user=self.user)
        tag2 = Tag.objects.create(name='Tag 2', user=self.user)
        self.task.tags.add(tag1, tag2)
        self.assertEqual(self.task.tags.count(), 2)

        # Remove all tags from the task
        data = {'tags': []}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 0)
        self.assertNotIn(tag1, task.tags.all())
        self.assertNotIn(tag2, task.tags.all())

    def test_update_task_with_tags(self):
        # Add some tags to the task
        tag1 = Tag.objects.create(name='Tag 1', user=self.user)
        tag2 = Tag.objects.create(name='Tag 2', user=self.user)
        self.task.tags.add(tag1, tag2)

        # Update the task's name and tags
        data = {
            'name': 'Updated Test Task',
            'tags': [{'name': 'Tag 2', 'user': self.user.id}, {'name': 'Tag 3', 'user': self.user.id}]
        }
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the task and its tags were updated
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.name, 'Updated Test Task')
        self.assertEqual(task.tags.count(), 2)
        self.assertNotIn(tag1, task.tags.all())
        self.assertIn(tag2, task.tags.all())
        self.assertIn('Tag 3', [tag.name for tag in task.tags.all()])

    def test_add_existing_tag_from_another_user_to_task(self):
        # Create a tag for a different user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='otheruser@example.com'
        )
        tag_name = 'Existing Tag'
        tag = Tag.objects.create(name=tag_name, user=other_user)

        # Add the existing tag to the task of the current user
        data = {'tags': [{'name': tag_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 1)

        # Verify that the added tag belongs to the current user
        added_tag = task.tags.first()
        self.assertEqual(added_tag.name, tag_name)
        self.assertEqual(added_tag.user, self.user)
        self.assertNotEqual(added_tag, tag)
        self.assertNotEqual(added_tag.id, tag.id)
        self.assertEqual(Tag.objects.filter(name=tag_name, user=self.user).count(), 1)
        self.assertEqual(Tag.objects.filter(name=tag_name, user=other_user).count(), 1)

    def test_remove_tag_from_task(self):
        tag = Tag.objects.create(name='Tag 2', user=self.user)
        self.task.tags.add(tag)
        self.assertEqual(self.task.tags.count(), 1)
        data = {'tags': [{'name': 'Tag 1', 'user': self.user.id}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.tags.count(), 1)
        self.assertNotIn(tag, task.tags.all())
        self.assertIn(tag, Tag.objects.all())

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

    def test_toggle_focus_invalid_task_id(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('task_toggle_focus', kwargs={'pk': self.task.id + 1})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_focus_unauthenticated_user(self):
        url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_toggle_focus_other_user_task(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_toggle_focus_deactivated_task(self):
        self.client.force_authenticate(user=self.user1)
        self.task.is_active = False
        self.task.save()
        url = reverse('task_toggle_focus', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.focus)

class TaskToggleDoneAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasktoggledoneuser1', 
            password='testpass123', 
            email='tasktoggledoneuser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasktoggledoneuser2', 
            password='testpass123', 
            email='tasktoggledoneuser2@example.com'
            )
        self.task = Task.objects.create(
            user=self.user1,
            name='Test Task',
            focus=False,
            done=False,
            readiness='inbox',
        )

    def test_toggle_done_valid_task(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('task_toggle_done', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertTrue(task.done)

    def test_toggle_done_invalid_task_id(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('task_toggle_done', kwargs={'pk': self.task.id + 1})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_done_unauthenticated_user(self):
        url = reverse('task_toggle_done', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_toggle_done_other_user_task(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('task_toggle_done', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_toggle_done_deactivated_task(self):
        self.client.force_authenticate(user=self.user1)
        self.task.is_active = False
        self.task.save()
        url = reverse('task_toggle_done', kwargs={'pk': self.task.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        task = Task.objects.get(id=self.task.id)
        self.assertFalse(task.done)

class TaskListFocusedAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistfocuseduser1', 
            password='testpass123', 
            email='tasklistfocuseduser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasklistfocuseduser2', 
            password='testpass123', 
            email='tasklistfocuseduser2@example.com'
            )
        self.focused_task_user1 = Task.objects.create(
            user=self.user1,
            name='Focused Task User1',
            focus=True,
            done=False,
            readiness='inbox',
        )
        self.not_focused_task_user1 = Task.objects.create(
            user=self.user1,
            name='Not Focused Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.focused_task_user2 = Task.objects.create(
            user=self.user2,
            name='Focused Task User2',
            focus=True,
            done=False,
            readiness='inbox',
        )

    def test_retrieve_focused_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('focused_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.focused_task_user1.name)

    def test_retrieve_focused_tasks_unauthenticated(self):
        url = reverse('focused_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_focused_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('focused_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.focused_task_user2.name)

    def test_retrieve_only_user_focused_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('focused_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.not_focused_task_user1.name)

    def test_retrieve_no_focused_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.focused_task_user1.focus = False
        self.focused_task_user1.save()
        url = reverse('focused_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_only_active_focused_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.focused_task_user1.is_active = False
        self.focused_task_user1.save()
        url = reverse('focused_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.focused_task_user1.is_active = True
        self.focused_task_user1.save()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.focused_task_user1.name)

class TaskListDoneAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistdoneuser1', 
            password='testpass123', 
            email='tasklistdoneuser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasklistdoneuser2', 
            password='testpass123', 
            email='tasklistdoneuser2@example.com'
            )
        self.done_task_user1 = Task.objects.create(
            user=self.user1,
            name='Done Task User1',
            focus=False,
            done=True,
            readiness='inbox',
        )
        self.not_done_task_user1 = Task.objects.create(
            user=self.user1,
            name='Not Done Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.done_task_user2 = Task.objects.create(
            user=self.user2,
            name='Done Task User2',
            focus=False,
            done=True,
            readiness='inbox',
        )

    def test_retrieve_done_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('done_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.done_task_user1.name)

    def test_retrieve_done_tasks_unauthenticated(self):
        url = reverse('done_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_done_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('done_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.done_task_user2.name)

    def test_retrieve_only_user_done_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('done_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.not_done_task_user1.name)

    def test_retrieve_no_done_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.done_task_user1.done = False
        self.done_task_user1.save()
        url = reverse('done_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_only_active_done_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.done_task_user1.is_active = False
        self.done_task_user1.save()
        url = reverse('done_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.done_task_user1.is_active = True
        self.done_task_user1.save()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.done_task_user1.name)

class TaskListReadinessInboxAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistreadinessinboxuser1', 
            password='testpass123', 
            email='tasklistreadinessinboxuser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasklistreadinessinboxuser2', 
            password='testpass123', 
            email='tasklistreadinessinboxuser2@example.com'
            )
        self.inbox_task_user1 = Task.objects.create(
            user=self.user1,
            name='Inbox Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.not_inbox_task_user1 = Task.objects.create(
            user=self.user1,
            name='Not Inbox Task User1',
            focus=False,
            done=False,
            readiness='sometime',
        )
        self.inbox_task_user2 = Task.objects.create(
            user=self.user2,
            name='Inbox Task User2',
            focus=False,
            done=False,
            readiness='inbox',
        )

    def test_retrieve_inbox_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('inbox_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.inbox_task_user1.name)

    def test_retrieve_inbox_tasks_unauthenticated(self):
        url = reverse('inbox_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_inbox_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('inbox_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.inbox_task_user2.name)

    def test_retrieve_only_user_inbox_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('inbox_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.not_inbox_task_user1.name)

    def test_retrieve_no_inbox_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.inbox_task_user1.readiness = 'sometime'
        self.inbox_task_user1.save()
        url = reverse('inbox_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_only_active_inbox_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.inbox_task_user1.is_active = False
        self.inbox_task_user1.save()
        url = reverse('inbox_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.inbox_task_user1.is_active = True
        self.inbox_task_user1.save()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.inbox_task_user1.name)

class TaskListReadinessSometimeAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistreadinesssometimeuser1', 
            password='testpass123', 
            email='tasklistreadinesssometimeuser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasklistreadinesssometimeuser2', 
            password='testpass123', 
            email='tasklistreadinesssometimeuser2@example.com'
            )
        self.sometime_task_user1 = Task.objects.create(
            user=self.user1,
            name='Sometime Task User1',
            focus=False,
            done=False,
            readiness='sometime',
        )
        self.not_sometime_task_user1 = Task.objects.create(
            user=self.user1,
            name='Not Sometime Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.sometime_task_user2 = Task.objects.create(
            user=self.user2,
            name='Sometime Task User2',
            focus=False,
            done=False,
            readiness='sometime',
        )

    def test_retrieve_sometime_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('sometime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.sometime_task_user1.name)

    def test_retrieve_sometime_tasks_unauthenticated(self):
        url = reverse('sometime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_sometime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('sometime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.sometime_task_user2.name)

    def test_retrieve_only_user_sometime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('sometime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.not_sometime_task_user1.name)

    def test_retrieve_no_sometime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.sometime_task_user1.readiness = 'inbox'
        self.sometime_task_user1.save()
        url = reverse('sometime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_only_active_sometime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.sometime_task_user1.is_active = False
        self.sometime_task_user1.save()
        url = reverse('sometime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.sometime_task_user1.is_active = True
        self.sometime_task_user1.save()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.sometime_task_user1.name)

class TaskListReadinessAnytimeAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistreadinessanytimeuser1', 
            password='testpass123', 
            email='tasklistreadinessanytimeuser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasklistreadinessanytimeuser2', 
            password='testpass123', 
            email='tasklistreadinessanytimeuser2@example.com'
            )
        self.anytime_task_user1 = Task.objects.create(
            user=self.user1,
            name='Anytime Task User1',
            focus=False,
            done=False,
            readiness='anytime',
        )
        self.not_anytime_task_user1 = Task.objects.create(
            user=self.user1,
            name='Not Anytime Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.anytime_task_user2 = Task.objects.create(
            user=self.user2,
            name='Anytime Task User2',
            focus=False,
            done=False,
            readiness='anytime',
        )

    def test_retrieve_anytime_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('anytime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.anytime_task_user1.name)

    def test_retrieve_anytime_tasks_unauthenticated(self):
        url = reverse('anytime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_anytime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('anytime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.anytime_task_user2.name)

    def test_retrieve_only_user_anytime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('anytime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.not_anytime_task_user1.name)

    def test_retrieve_no_anytime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.anytime_task_user1.readiness = 'inbox'
        self.anytime_task_user1.save()
        url = reverse('anytime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_only_active_anytime_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.anytime_task_user1.is_active = False
        self.anytime_task_user1.save()
        url = reverse('anytime_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class TaskListReadinessWaitingAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistreadinesswaitinguser1', 
            password='testpass123', 
            email='tasklistreadinesswaitinguser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='tasklistreadinesswaitinguser2', 
            password='testpass123', 
            email='tasklistreadinesswaitinguser2@example.com'
            )
        self.waiting_task_user1 = Task.objects.create(
            user=self.user1,
            name='Waiting Task User1',
            focus=False,
            done=False,
            readiness='waiting',
        )
        self.not_waiting_task_user1 = Task.objects.create(
            user=self.user1,
            name='Not Waiting Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.waiting_task_user2 = Task.objects.create(
            user=self.user2,
            name='Waiting Task User2',
            focus=False,
            done=False,
            readiness='waiting',
        )

    def test_retrieve_waiting_tasks_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('waiting_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.waiting_task_user1.name)

    def test_retrieve_waiting_tasks_unauthenticated(self):
        url = reverse('waiting_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_waiting_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('waiting_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.waiting_task_user2.name)

    def test_retrieve_only_user_waiting_tasks(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('waiting_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], self.not_waiting_task_user1.name)

    def test_retrieve_no_waiting_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.waiting_task_user1.readiness = 'inbox'
        self.waiting_task_user1.save()
        url = reverse('waiting_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_only_active_waiting_tasks(self):
        self.client.force_authenticate(user=self.user1)
        self.waiting_task_user1.is_active = False
        self.waiting_task_user1.save()
        url = reverse('waiting_task_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

class TaskDisableAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='taskdisableuser1', 
            password='testpass123', 
            email='taskdisableuser1@example.com'
            )
        self.user2 = User.objects.create_user(
            username='taskdisableuser2', 
            password='testpass123', 
            email='taskdisableuser2@example.com'
            )
        self.task_user1 = Task.objects.create(
            user=self.user1,
            name='Test Task User1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.task_user2 = Task.objects.create(
            user=self.user2,
            name='Test Task User2',
            focus=False,
            done=False,
            readiness='inbox',
        )

    def test_disable_own_task_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('task_disable', kwargs={'pk': self.task_user1.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task_user1.id)
        self.assertFalse(task.is_active)

    def test_disable_other_user_task_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        self.assertEqual(self.task_user2.user, self.user2)
        url = reverse('task_disable', kwargs={'pk': self.task_user2.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        task = Task.objects.get(id=self.task_user2.id)
        self.assertTrue(task.is_active)

    def test_disable_already_disabled_task(self):
        self.client.force_authenticate(user=self.user1)
        self.task_user1.is_active = False
        self.task_user1.save()
        url = reverse('task_disable', kwargs={'pk': self.task_user1.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_disable_non_existent_task(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('task_disable', kwargs={'pk': 99999})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_disable_unauthenticated_user(self):
        url = reverse('task_disable', kwargs={'pk': self.task_user1.id})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TaskListAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='tasklistuser1',
            password='testpass123',
            email='tasklistuser1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='tasklistuser2',
            password='testpass123',
            email='tasklistuser2@example.com'
        )
        self.task1 = Task.objects.create(
            user=self.user1,
            name='Task 1',
            focus=False,
            done=False,
            readiness='inbox',
        )
        self.task2 = Task.objects.create(
            user=self.user2,
            name='Task 2',
            focus=True,
            done=False,
            readiness='inbox',
        )
        self.task3 = Task.objects.create(
            user=self.user1,
            name='Task 3',
            focus=True,
            done=True,
            readiness='anytime',
        )

    def test_retrieve_own_tasks_authenticated(self):
        """
        Test that an authenticated user can retrieve their own tasks
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('task_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.task1.name)
        self.assertEqual(response.data[1]['name'], self.task3.name)

    def test_retrieve_tasks_unauthenticated(self):
        """
        Test that a non-authenticated user cannot retrieve any tasks
        """
        response = self.client.get(reverse('task_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_other_user_tasks_authenticated(self):
        """
        Test that a user cannot retrieve tasks belonging to another user
        """
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('task_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.task1.name)
        self.assertEqual(response.data[1]['name'], self.task3.name)

        # try to retrieve other user's task
        self.client.force_authenticate(user=self.user1)
        url = reverse('task_detail', kwargs={'pk': self.task2.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_active_tasks_only(self):
        """
        Test that the response contains all active tasks belonging to the authenticated user
        """
        self.client.force_authenticate(user=self.user1)
        self.task1.is_active = False
        self.task1.save()

        response = self.client.get(reverse('task_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.task3.name)

class TagCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tagcreateuser', password='testpass123', email='tagcreateuser@example.com')

    def test_create_valid_tag(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('tag_create')
        data = {
            'name': 'market',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'market')

class TagDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.tag = Tag.objects.create(name='Test Tag', user=self.user)
        self.url = reverse('tag_detail', kwargs={'pk': self.tag.pk})

    def test_get_valid_tag(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.tag.id)
        self.assertEqual(response.data['name'], self.tag.name)

    def test_get_invalid_tag(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('tag_detail', kwargs={'pk': self.tag.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tag_from_different_user(self):
        other_user = User.objects.create_user(username='testuser2', password='testpass123', email='testuser2@example.com')
        tag = Tag.objects.create(name='Test Tag 2', user=other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('tag_detail', kwargs={'pk': tag.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tag_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TagUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tagupdateuser', password='testpass123', email='tagupdateuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.tag = Tag.objects.create(name='market', user=self.user)

    def test_update_valid_tag(self):
        url = reverse('tag_update', kwargs={'pk': self.tag.id})
        data = {
            'name': 'grocery',
            'is_active': False,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(tag.name, 'grocery')
        self.assertFalse(tag.is_active)

class TagDisableAPIViewTest(APITestCase):

    def setUp(self):
        # Create a test user and authentication token
        self.user = User.objects.create_user(username='tagdisableuser1', password='testpass', email='tagdisableuser1@example.com')

        # Create some test Tag objects
        self.tag1 = Tag.objects.create(
            user=self.user,
            name='market', 
        )
        self.tag2 = Tag.objects.create(
            user=self.user,
            name='downtown', 
        )

        self.client.force_authenticate(user=self.user)

    def test_disable_active_tag(self):
        # Disable an active tag
        url = reverse('tag_disable', kwargs={'pk': self.tag1.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the tag has been disabled
        tag = Tag.objects.get(id=self.tag1.id)
        self.assertFalse(tag.is_active)

    def test_disable_inactive_tag(self):
        # Try to disable an inactive tag
        self.tag2.is_active = False
        self.tag2.save()

        url = reverse('tag_disable', kwargs={'pk': self.tag2.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disable_tag_of_another_user(self):
        # Try to disable a tag that belongs to another user
        user2 = User.objects.create_user(username='tagdisableuser2', password='testpass', email='tagdisableuser2@example.com')
        tag3 = Tag.objects.create(
            user=user2,
            name='beach', 
        )
        self.client.force_authenticate(user=self.user)

        url = reverse('tag_disable', kwargs={'pk': tag3.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disable_nonexistent_tag(self):
        # Try to disable a tag that doesn't exist
        url = reverse('tag_disable', kwargs={'pk': 999})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TagListAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='testpass123', email='user2@example.com')
        self.tag1 = Tag.objects.create(name='tag1', user=self.user1)
        self.tag2 = Tag.objects.create(name='tag2', user=self.user1)
        self.tag3 = Tag.objects.create(name='tag3', user=self.user2)

    def test_list_tags(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('tag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        tag_names = [tag['name'] for tag in response.data]
        self.assertIn(self.tag1.name, tag_names)
        self.assertIn(self.tag2.name, tag_names)
        self.assertNotIn(self.tag3.name, tag_names)

    def test_list_tags_unauthenticated(self):
        url = reverse('tag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tags_different_user(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('tag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag_names = [tag['name'] for tag in response.data]
        self.assertNotIn(self.tag3.name, tag_names)
