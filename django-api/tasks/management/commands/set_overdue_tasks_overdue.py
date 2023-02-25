from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task


class Command(BaseCommand):
    help = 'Toggle overdue for overdue tasks'

    def handle(self, *args, **options):
        now = timezone.now().date()
        overdue_tasks = Task.objects.filter(due_date__lt=now, overdue=False, is_active=True)
        overdue_tasks.update(overdue=True)