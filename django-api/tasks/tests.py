import time
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from datetime import timedelta
from tasks.models import Task
from tasks.management.commands.toggle_overdue import Command as ToggleOverdueCommand
from tasks.management.commands.toggle_focus import Command as ToggleFocusCommand



class CronJobOverdueTaskTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='OverdueTasktestuser',
            password='testpass',
            email='OverdueTasktestuser@example.com'
        )

        # Create a task that should be updated by the cron job
        self.overdue_task = Task.objects.create(
            user=self.user,
            name='Task 1',
            focus=False,
            done=False,
            readiness='inbox',
            due_date=timezone.now().date() - timedelta(days=1)
        )

        # Create a task that should not be updated by the cron job
        self.non_overdue_task = Task.objects.create(
            user=self.user,
            name='Task 2',
            focus=False,
            done=False,
            readiness='inbox',
            due_date=timezone.now().date() + timedelta(days=1)
        )
    def test_cron_job_toggle_overdue_tasks(self):
        # Create instances of the toggle overdue and toggle focus commands
        toggle_overdue_command = ToggleOverdueCommand()
        toggle_focus_command = ToggleFocusCommand()

        # Call the handle method to execute the commands
        toggle_overdue_command.handle()
        toggle_focus_command.handle()

        # Wait for a few seconds to ensure that the commands have completed
        time.sleep(5)

        # Retrieve the task and check that the relevant fields have been updated
        updated_task = Task.objects.get(id=self.overdue_task.id)
        self.assertTrue(updated_task.overdue)

        # Retrieve the task and check that the relevant fields have not been updated
        updated_task2 = Task.objects.get(id=self.non_overdue_task.id)
        self.assertFalse(updated_task2.overdue)


