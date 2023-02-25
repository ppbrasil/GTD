from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task


class Command(BaseCommand):
    help = 'Toggle focus for tasks due today'

    def handle(self, *args, **options):
        now = timezone.now().date()
        tasks_due_today = Task.objects.filter(due_date__lte=now, focus=False, is_active=True)
        tasks_due_today.update(focus=True)
