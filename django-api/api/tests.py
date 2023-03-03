import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from tasks.models import Task, SimpleTag, Person

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

    def test_create_task_with_simpletags(self):
        self.client.force_authenticate(user=self.user)
        # Create a task with simpletags
        url = reverse('task_create')
        data = {
            'name': 'Test task',
            'simpletags': [{'name': 'simpletag1'}, {'name': 'simpletag2'}]
        }
        print(data)
        response = self.client.post(url, data, format='json')
        print('Request data:', json.dumps(data))
        print('Response data:', response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the task and simpletags have been created
        task = Task.objects.get(name='Test task')
        print(task.simpletags.all())
        self.assertEqual(task.name, 'Test task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.simpletags.count(), 2)
        self.assertTrue(task.simpletags.filter(name='simpletag1').exists())
        self.assertTrue(task.simpletags.filter(name='simpletag2').exists())
        
    def test_create_task_with_persons(self):
        self.client.force_authenticate(user=self.user)
        # Create a task with persons
        url = reverse('task_create')
        data = {
            'name': 'Test task',
            'persons': [{'name': 'person1'}, {'name': 'person2'}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the task and persons have been created
        task = Task.objects.get(name='Test task')
        self.assertEqual(task.name, 'Test task')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.persons.count(), 2)
        self.assertTrue(task.persons.filter(name='person1').exists())
        self.assertTrue(task.persons.filter(name='person2').exists())

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

    def test_add_new_simpletag_to_task(self):
        # Add existing simpletag to task's simpletag list
        existing_simpletag_data = {'name': 'SimpleTag 1', 'user': self.user.id}
        data = {'simpletags': [existing_simpletag_data]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 1)
        self.assertIn(existing_simpletag_data['name'], [simpletag.name for simpletag in task.simpletags.all()])

        # Add new simpletag to task's simpletag list
        new_simpletag_data = {'name': 'New SimpleTag', 'user': self.user.id}
        data = {'simpletags': [existing_simpletag_data, new_simpletag_data]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 2)
        self.assertIn(existing_simpletag_data['name'], [simpletag.name for simpletag in task.simpletags.all()])
        self.assertIn(new_simpletag_data['name'], [simpletag.name for simpletag in task.simpletags.all()])

    def test_add_new_person_to_task(self):
        # Add existing person to task's person list
        existing_person_data = {'name': 'Person 1', 'user': self.user.id}
        data = {'persons': [existing_person_data]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.persons.count(), 1)
        self.assertIn(existing_person_data['name'], [person.name for person in task.persons.all()])

        # Add new person to task's person list
        new_person_data = {'name': 'New Person', 'user': self.user.id}
        data = {'persons': [existing_person_data, new_person_data]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.persons.count(), 2)
        self.assertIn(existing_person_data['name'], [person.name for person in task.persons.all()])
        self.assertIn(new_person_data['name'], [person.name for person in task.persons.all()])

    def test_add_existing_simpletag_to_task(self):
        # Create an existing simpletag
        existing_simpletag_name = 'Existing SimpleTag'
        existing_simpletag = SimpleTag.objects.create(name=existing_simpletag_name, user=self.user)
        
        # Add existing simpletag to task's simpletag list
        data = {'simpletags': [{'name': existing_simpletag_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 1)
        self.assertIn(existing_simpletag, task.simpletags.all())

    def test_add_existing_person_to_task(self):
        # Create an existing person
        existing_person_name = 'Existing Person'
        existing_person = Person.objects.create(name=existing_person_name, user=self.user)

        # Add existing person to task's person list
        data = {'persons': [{'name': existing_person_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.persons.count(), 1)
        self.assertIn(existing_person, task.persons.all())

    def test_create_new_simpletag_while_trying_to_add_simpletag_with_same_name_but_from_different_user_to_task(self):
        another_user=User.objects.create()

        # Create an existing simpletag with the same name but a different user
        existing_simpletag_name = 'SimpleTag from other user'
        existing_simpletag = SimpleTag.objects.create(name=existing_simpletag_name, user=another_user)
        
        # Add existing simpletag to task's simpletag list
        data = {'simpletags': [{'name': existing_simpletag_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 1)
        self.assertNotIn(existing_simpletag, task.simpletags.all())
        self.assertIn(existing_simpletag_name, [simpletag.name for simpletag in task.simpletags.all()])

    def test_create_new_person_while_trying_to_add_person_with_same_name_but_from_different_user_to_task(self):
        another_user=User.objects.create()

        # Create an existing person with the same name but a different user
        existing_person_name = 'Person from other user'
        existing_person = Person.objects.create(name=existing_person_name, user=another_user)
        
        # Add existing person to task's person list
        data = {'persons': [{'name': existing_person_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.persons.count(), 1)
        self.assertNotIn(existing_person, task.persons.all())
        self.assertIn(existing_person_name, [person.name for person in task.persons.all()])

    def test_remove_all_simpletags_from_task(self):
        # Add some simpletags to the task
        simpletag1 = SimpleTag.objects.create(name='SimpleTag 1', user=self.user)
        simpletag2 = SimpleTag.objects.create(name='SimpleTag 2', user=self.user)
        self.task.simpletags.add(simpletag1, simpletag2)
        self.assertEqual(self.task.simpletags.count(), 2)

        # Remove all simpletags from the task
        data = {'simpletags': []}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 0)
        self.assertNotIn(simpletag1, task.simpletags.all())
        self.assertNotIn(simpletag2, task.simpletags.all())

    def test_remove_all_persons_from_task(self):
        # Add some persons to the task
        person1 = Person.objects.create(name='Person 1', user=self.user)
        person2 = Person.objects.create(name='Person 2', user=self.user)
        self.task.persons.add(person1, person2)
        self.assertEqual(self.task.persons.count(), 2)

        # Remove all persons from the task
        data = {'persons': []}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.persons.count(), 0)
        self.assertNotIn(person1, task.persons.all())
        self.assertNotIn(person2, task.persons.all())

    def test_update_task_with_simpletags(self):
        # Add some simpletags to the task
        simpletag1 = SimpleTag.objects.create(name='SimpleTag 1', user=self.user)
        simpletag2 = SimpleTag.objects.create(name='SimpleTag 2', user=self.user)
        self.task.simpletags.add(simpletag1, simpletag2)

        # Update the task's name and simpletags
        data = {
            'name': 'Updated Test Task',
            'simpletags': [{'name': 'SimpleTag 2', 'user': self.user.id}, {'name': 'SimpleTag 3', 'user': self.user.id}]
        }
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the task and its simpletags were updated
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.name, 'Updated Test Task')
        self.assertEqual(task.simpletags.count(), 2)
        self.assertNotIn(simpletag1, task.simpletags.all())
        self.assertIn(simpletag2, task.simpletags.all())
        self.assertIn('SimpleTag 3', [simpletag.name for simpletag in task.simpletags.all()])

    def test_update_task_with_persons(self):
        # Add some persons to the task
        person1 = Person.objects.create(name='Person 1', user=self.user)
        person2 = Person.objects.create(name='Person 2', user=self.user)
        self.task.persons.add(person1, person2)

        # Update the task's name and persons
        data = {
            'name': 'Updated Test Task',
            'persons': [{'name': 'Person 2'}, {'name': 'Person 3'}]
        }
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the task and its persons were updated
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.name, 'Updated Test Task')
        self.assertEqual(task.persons.count(), 2)
        self.assertNotIn(person1, task.persons.all())
        self.assertIn(person2, task.persons.all())
        self.assertIn('Person 3', [person.name for person in task.persons.all()])

    def test_add_existing_simpletag_from_another_user_to_task(self):
        # Create a simpletag for a different user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='otheruser@example.com'
        )
        simpletag_name = 'Existing SimpleTag'
        simpletag = SimpleTag.objects.create(name=simpletag_name, user=other_user)

        # Add the existing simpletag to the task of the current user
        data = {'simpletags': [{'name': simpletag_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 1)

        # Verify that the added simpletag belongs to the current user
        added_simpletag = task.simpletags.first()
        self.assertEqual(added_simpletag.name, simpletag_name)
        self.assertEqual(added_simpletag.user, self.user)
        self.assertNotEqual(added_simpletag, simpletag)
        self.assertNotEqual(added_simpletag.id, simpletag.id)
        self.assertEqual(SimpleTag.objects.filter(name=simpletag_name, user=self.user).count(), 1)
        self.assertEqual(SimpleTag.objects.filter(name=simpletag_name, user=other_user).count(), 1)

    def test_add_existing_person_from_another_user_to_task(self):
        # Create a person for a different user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='otheruser@example.com'
        )
        person_name = 'Existing Person'
        person = Person.objects.create(name=person_name, user=other_user)

        # Add the existing person to the task of the current user
        data = {'persons': [{'name': person_name}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.persons.count(), 1)

        # Verify that the added person belongs to the current user
        added_person = task.persons.first()
        self.assertEqual(added_person.name, person_name)
        self.assertEqual(added_person.user, self.user)
        self.assertNotEqual(added_person, person)
        self.assertNotEqual(added_person.id, person.id)
        self.assertEqual(Person.objects.filter(name=person_name, user=self.user).count(), 1)
        self.assertEqual(Person.objects.filter(name=person_name, user=other_user).count(), 1)

    def test_remove_simpletag_from_task(self):
        simpletag = SimpleTag.objects.create(name='SimpleTag 2', user=self.user)
        self.task.simpletags.add(simpletag)
        self.assertEqual(self.task.simpletags.count(), 1)
        data = {'simpletags': [{'name': 'SimpleTag 1', 'user': self.user.id}]}
        url = reverse('task_update', kwargs={'pk': self.task.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.simpletags.count(), 1)
        self.assertNotIn(simpletag, task.simpletags.all())
        self.assertIn(simpletag, SimpleTag.objects.all())

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

class SimpleTagCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='simpletagcreateuser', password='testpass123', email='simpletagcreateuser@example.com')

    def test_create_valid_simpletag(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('simpletag_create')
        data = {
            'name': 'market',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'market')

class SimpleTagDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.simpletag = SimpleTag.objects.create(name='Test SimpleTag', user=self.user)
        self.url = reverse('simpletag_detail', kwargs={'pk': self.simpletag.pk})

    def test_get_valid_simpletag(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.simpletag.id)
        self.assertEqual(response.data['name'], self.simpletag.name)

    def test_get_invalid_simpletag(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('simpletag_detail', kwargs={'pk': self.simpletag.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_simpletag_from_different_user(self):
        other_user = User.objects.create_user(username='testuser2', password='testpass123', email='testuser2@example.com')
        simpletag = SimpleTag.objects.create(name='Test SimpleTag 2', user=other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('simpletag_detail', kwargs={'pk': simpletag.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_simpletag_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class SimpleTagUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='simpletagupdateuser', password='testpass123', email='simpletagupdateuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.simpletag = SimpleTag.objects.create(name='market', user=self.user)

    def test_update_valid_simpletag(self):
        url = reverse('simpletag_update', kwargs={'pk': self.simpletag.id})
        data = {
            'name': 'grocery',
            'is_active': False,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        simpletag = SimpleTag.objects.get(id=self.simpletag.id)
        self.assertEqual(simpletag.name, 'grocery')
        self.assertFalse(simpletag.is_active)

class SimpleTagDisableAPIViewTest(APITestCase):

    def setUp(self):
        # Create a test user and authentication token
        self.user = User.objects.create_user(username='simpletagdisableuser1', password='testpass', email='simpletagdisableuser1@example.com')

        # Create some test SimpleTag objects
        self.simpletag1 = SimpleTag.objects.create(
            user=self.user,
            name='market', 
        )
        self.simpletag2 = SimpleTag.objects.create(
            user=self.user,
            name='downtown', 
        )

        self.client.force_authenticate(user=self.user)

    def test_disable_active_simpletag(self):
        # Disable an active simpletag
        url = reverse('simpletag_disable', kwargs={'pk': self.simpletag1.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the simpletag has been disabled
        simpletag = SimpleTag.objects.get(id=self.simpletag1.id)
        self.assertFalse(simpletag.is_active)

    def test_disable_inactive_simpletag(self):
        # Try to disable an inactive simpletag
        self.simpletag2.is_active = False
        self.simpletag2.save()

        url = reverse('simpletag_disable', kwargs={'pk': self.simpletag2.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disable_simpletag_of_another_user(self):
        # Try to disable a simpletag that belongs to another user
        user2 = User.objects.create_user(username='simpletagdisableuser2', password='testpass', email='simpletagdisableuser2@example.com')
        simpletag3 = SimpleTag.objects.create(
            user=user2,
            name='beach', 
        )
        self.client.force_authenticate(user=self.user)

        url = reverse('simpletag_disable', kwargs={'pk': simpletag3.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disable_nonexistent_simpletag(self):
        # Try to disable a simpletag that doesn't exist
        url = reverse('simpletag_disable', kwargs={'pk': 999})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SimpleTagListAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='testpass123', email='user2@example.com')
        self.simpletag1 = SimpleTag.objects.create(name='simpletag1', user=self.user1)
        self.simpletag2 = SimpleTag.objects.create(name='simpletag2', user=self.user1)
        self.simpletag3 = SimpleTag.objects.create(name='simpletag3', user=self.user2)

    def test_list_simpletags(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('simpletag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        simpletag_names = [simpletag['name'] for simpletag in response.data]
        self.assertIn(self.simpletag1.name, simpletag_names)
        self.assertIn(self.simpletag2.name, simpletag_names)
        self.assertNotIn(self.simpletag3.name, simpletag_names)

    def test_list_simpletags_unauthenticated(self):
        url = reverse('simpletag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_simpletags_different_user(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('simpletag_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        simpletag_names = [simpletag['name'] for simpletag in response.data]
        self.assertNotIn(self.simpletag3.name, simpletag_names)

class PersonCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='personcreateuser', password='testpass123', email='personcreateuser@example.com')

    def test_create_valid_person(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('person_create')
        data = {
            'name': 'John Doe',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'John Doe')

class PersonDetailAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='testuser@example.com')
        self.person = Person.objects.create(name='Test Person', user=self.user)
        self.url = reverse('person_detail', kwargs={'pk': self.person.pk})

    def test_get_valid_person(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.person.id)
        self.assertEqual(response.data['name'], self.person.name)

    def test_get_invalid_person(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('person_detail', kwargs={'pk': self.person.pk + 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_person_from_different_user(self):
        other_user = User.objects.create_user(username='testuser2', password='testpass123', email='testuser2@example.com')
        person = Person.objects.create(name='Test Person 2', user=other_user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('person_detail', kwargs={'pk': person.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_person_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PersonUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='personupdateuser', password='testpass123', email='personupdateuser@example.com')
        self.client.force_authenticate(user=self.user)
        self.person = Person.objects.create(name='John', user=self.user)

    def test_update_valid_person(self):
        url = reverse('person_update', kwargs={'pk': self.person.id})
        data = {
            'name': 'Jane',
            'is_active': False,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person = Person.objects.get(id=self.person.id)
        self.assertEqual(person.name, 'Jane')
        self.assertFalse(person.is_active)

class PersonDisableAPIViewTest(APITestCase):

    def setUp(self):
        # Create a test user and authentication token
        self.user = User.objects.create_user(username='persondisableuser1', password='testpass', email='persondisableuser1@example.com')

        # Create some test Person objects
        self.person1 = Person.objects.create(
            user=self.user,
            name='Alice', 
        )
        self.person2 = Person.objects.create(
            user=self.user,
            name='Bob', 
        )

        self.client.force_authenticate(user=self.user)

    def test_disable_active_person(self):
        # Disable an active person
        url = reverse('person_disable', kwargs={'pk': self.person1.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the person has been disabled
        person = Person.objects.get(id=self.person1.id)
        self.assertFalse(person.is_active)

    def test_disable_inactive_person(self):
        # Try to disable an inactive person
        self.person2.is_active = False
        self.person2.save()

        url = reverse('person_disable', kwargs={'pk': self.person2.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disable_person_of_another_user(self):
        # Try to disable a person that belongs to another user
        user2 = User.objects.create_user(username='persondisableuser2', password='testpass', email='persondisableuser2@example.com')
        person3 = Person.objects.create(
            user=user2,
            name='Charlie', 
        )
        self.client.force_authenticate(user=self.user)

        url = reverse('person_disable', kwargs={'pk': person3.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_disable_nonexistent_person(self):
        # Try to disable a person that doesn't exist
        url = reverse('person_disable', kwargs={'pk': 999})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PersonListAPIViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='testpass123', email='user2@example.com')
        self.person1 = Person.objects.create(name='person1', user=self.user1)
        self.person2 = Person.objects.create(name='person2', user=self.user1)
        self.person3 = Person.objects.create(name='person3', user=self.user2)

    def test_list_people(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('person_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        person_names = [person['name'] for person in response.data]
        self.assertIn(self.person1.name, person_names)
        self.assertIn(self.person2.name, person_names)
        self.assertNotIn(self.person3.name, person_names)

    def test_list_people_unauthenticated(self):
        url = reverse('person_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_people_different_user(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('person_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_names = [person['name'] for person in response.data]
        self.assertNotIn(self.person3.name, person_names)

