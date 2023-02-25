from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task


class Command(BaseCommand):
    help = 'Update readiness for waiting tasks'

    def handle(self, *args, **options):
        now = timezone.now()
        waiting_tasks = Task.objects.filter(
            waiting_for__isnull=False, 
            waiting_for__waiting_date__lte=now, 
            is_active=True, 
            readiness='waiting'
            )
        waiting_tasks.update(readiness='anytime')
