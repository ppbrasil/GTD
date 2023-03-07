from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from tasks.models import Task


class SetAnytimeTasksWaitingForNowTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='SetAnytimeTasksWaitingForNowTestCaseUser',
            password='testpass123',
            email='SetAnytimeTasksWaitingForNowTestCaseUserEmail@example.com'
        )

    def test_tasks_with_waiting_for_before_or_equal_now_are_updated_to_anytime(self):
        task_waiting = Task.objects.create(readiness='waiting', waiting_for_time=timezone.now(), user=self.user1, is_active=True)

        # Call the command handle method to execute the script
        call_command('set_anytime_tasks_waiting_for_now')

        # Refresh the task from the database and check if the readiness has been updated
        task_waiting.refresh_from_db()
        self.assertEqual(task_waiting.readiness, 'anytime')
    
    def test_tasks_with_waiting_for_after_now_are_not_updated_to_anytime(self):
        task_waiting = Task.objects.create(readiness='waiting', waiting_for_time=timezone.now() + timezone.timedelta(minutes=10), user=self.user1, is_active=True)

        # Call the command handle method to execute the script
        call_command('set_anytime_tasks_waiting_for_now')

        # Refresh the task from the database and check if the readiness has not been updated
        task_waiting.refresh_from_db()
        self.assertEqual(task_waiting.readiness, 'waiting')

    def test_tasks_with_waiting_for_null_are_not_updated_to_anytime(self):
        task_inbox = Task.objects.create(readiness='inbox', user=self.user1, is_active=True)

        # Call the command handle method to execute the script
        call_command('set_anytime_tasks_waiting_for_now')

        # Refresh the task from the database and check if the readiness has not been updated
        task_inbox.refresh_from_db()
        self.assertEqual(task_inbox.readiness, 'inbox')

    def test_tasks_with_is_active_set_to_false_are_not_updated_to_anytime(self):
        task_waiting_inactive = Task.objects.create(readiness='waiting', waiting_for_time=timezone.now(), user=self.user1, is_active=False)

        # Call the command handle method to execute the script
        call_command('set_anytime_tasks_waiting_for_now')

        # Refresh the task from the database and check if the readiness has not been updated
        task_waiting_inactive.refresh_from_db()
        self.assertEqual(task_waiting_inactive.readiness, 'waiting')

class SetFocusTasksDueTodayTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='SetFocusTasksDueTodayTestCaseUser',
            password='testpass123',
            email='SetFocusTasksDueTodayTestCaseUserEmail@example.com'
        )

    def test_tasks_with_due_date_set_to_today_are_updated_to_have_focus_set_to_true(self):
        today = timezone.now().date()
        task_due_today = Task.objects.create(
            name='Task due today',
            user=self.user1,
            due_date=today,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_focus_tasks_due_today')

        # Refresh the task from the database and check if focus has been updated to True
        task_due_today.refresh_from_db()
        self.assertTrue(task_due_today.focus)

    def test_tasks_with_due_date_set_before_today_are_updated_to_have_focus_set_to_true(self):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        task_due_yesterday = Task.objects.create(
            name='Task due yesterday',
            user=self.user1,
            due_date=yesterday,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_focus_tasks_due_today')

        # Refresh the task from the database and check if focus has been updated to True
        task_due_yesterday.refresh_from_db()
        self.assertTrue(task_due_yesterday.focus)

    def test_tasks_with_due_date_set_after_today_are_not_updated_to_have_focus_set_to_true(self):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        task_due_tomorrow = Task.objects.create(
            name='Task due tomorrow',
            user=self.user1,
            due_date=tomorrow,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_focus_tasks_due_today')

        # Refresh the task from the database and check if focus has not been updated to True
        task_due_tomorrow.refresh_from_db()
        self.assertFalse(task_due_tomorrow.focus)

    def test_tasks_with_focus_already_set_to_true_are_not_updated_to_false_by_this_script(self):
        today = timezone.now().date()
        task_due_today = Task.objects.create(
            name='Task due today',
            user=self.user1,
            due_date=today,
            focus=True,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_focus_tasks_due_today')

        # Refresh the task from the database and check if focus has not been updated to False
        task_due_today.refresh_from_db()
        self.assertTrue(task_due_today.focus)

    def test_tasks_with_is_active_set_to_false_are_not_updated_by_this_script(self):
        today = timezone.now().date()
        task_due_today_inactive = Task.objects.create(
            name='Task due today (inactive)',
            user=self.user1,
            due_date=today,
            is_active=False
        )

        # Call the command handle method to execute the script
        call_command('set_focus_tasks_due_today')

        # Refresh the task from the database and check if focus has not been updated
        task_due_today_inactive.refresh_from_db()
        self.assertFalse(task_due_today_inactive.focus)

class SetOverdueTasksOverdueTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='SetOverdueTasksOverdueTestCaseUser',
            password='testpass123',
            email='SetOverdueTasksOverdueTestCaseUserEmail@example.com'
        )

    def test_tasks_with_due_date_set_before_today_are_updated_to_have_overdue_set_to_true(self):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        task_overdue = Task.objects.create(
            name='Task overdue',
            user=self.user1,
            due_date=yesterday,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_overdue_tasks_overdue')

        # Refresh the task from the database and check if overdue has been updated to True
        task_overdue.refresh_from_db()
        self.assertTrue(task_overdue.overdue)

    def test_tasks_with_due_date_set_today_are_not_updated_to_have_overdue_set_to_true(self):
        today = timezone.now().date()
        task_due_today = Task.objects.create(
            name='Task due today',
            user=self.user1,
            due_date=today,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_overdue_tasks_overdue')

        # Refresh the task from the database and check if overdue has not been updated to True
        task_due_today.refresh_from_db()
        self.assertFalse(task_due_today.overdue)

    def test_tasks_with_due_date_set_after_today_are_not_updated_to_have_overdue_set_to_true(self):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        task_not_overdue = Task.objects.create(
            name='Task not overdue',
            user=self.user1,
            due_date=tomorrow,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_overdue_tasks_overdue')

        # Refresh the task from the database and check if overdue has not been updated to True
        task_not_overdue.refresh_from_db()
        self.assertFalse(task_not_overdue.overdue)

    def test_tasks_with_overdue_already_set_to_true_are_not_updated_by_this_script(self):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        task_overdue = Task.objects.create(
            name='Task overdue',
            user=self.user1,
            due_date=yesterday,
            overdue=True,
            is_active=True
        )

        # Call the command handle method to execute the script
        call_command('set_overdue_tasks_overdue')

        # Refresh the task from the database and check if overdue has not been updated to False
        task_overdue.refresh_from_db()
        self.assertTrue(task_overdue.overdue)

    def test_tasks_with_is_active_set_to_false_are_not_updated_by_this_script(self):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        task_overdue_inactive = Task.objects.create(
            name='Task overdue (inactive)',
            user=self.user1,
            due_date=yesterday,
            is_active=False
        )

        # Call the command handle method to execute the script
        call_command('set_overdue_tasks_overdue')

        # Refresh the task from the database and check if overdue has not been updated
        task_overdue_inactive.refresh_from_db()
        self.assertFalse(task_overdue_inactive.overdue)
