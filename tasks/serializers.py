import warnings
from django.utils import timezone
from rest_framework import serializers

from .models import Task

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'name',
        ]

def validate_due_date(value):
    if value and value < timezone.now().date():
        warnings.warn("Due date in the past.")
    return value

def validate_reminder(value):
    if value and value < timezone.now():
        warnings.warn("Reminder in the past.")
    return value


class WaitingForSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'person',
            'due_date',
        ]

class TaskSerializer(serializers.ModelSerializer):
    waiting_for = WaitingForSerializer(read_only=True)
    due_date = serializers.DateField(validators=[validate_due_date], required=False)
    reminder = serializers.DateTimeField(validators=[validate_reminder], required=False)

    class Meta:
        model = Task
        fields = [
            'name',
            'focus',
            'done',
            'waiting_for',
            'due_date',
            'reminder',
            'readiness',
            'notes',
        ]