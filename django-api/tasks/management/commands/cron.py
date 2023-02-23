from django.utils import timezone
from tasks.models import Task

def toggle_overdue_tasks():
    now = timezone.now().date()

    tasks_due_today = Task.objects.filter(due_date__date=now, focus=False, is_active=True)
    tasks_due_today.update(focus=True)

def toogle_focus_for_tasks_dueing_today():
    now = timezone.now().date()

    overdue_tasks = Task.objects.filter(due_date__lt=now, overdue=False, is_active=True)
    overdue_tasks.update(overdue=True)