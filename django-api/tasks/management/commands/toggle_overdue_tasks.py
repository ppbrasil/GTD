from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from tasks.models import Task

class Command(BaseCommand):
    help = 'Toggle overdue and focus flags for tasks'

    def handle(self, *args, **options):
        now = datetime.now().date()
        today = now + timedelta(days=1)

        tasks_due_today = Task.objects.filter(due_date__date=now, focus=False)
        tasks_due_today.update(focus=True)

        overdue_tasks = Task.objects.filter(due_date__lt=now, overdue=False)
        overdue_tasks.update(overdue=True)

        self.stdout.write(self.style.SUCCESS('Successfully updated focus and overdue flags for tasks'))
