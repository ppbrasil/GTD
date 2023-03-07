from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task


class Command(BaseCommand):
    help = 'Update readiness for waiting tasks'

    def handle(self, *args, **options):
        now = timezone.now()
        waiting_tasks = Task.objects.filter(
            waiting_for_time__isnull=False, 
            waiting_for_time__lte=now, 
            is_active=True, 
            readiness='waiting'
            )
        waiting_tasks.update(readiness='anytime')
