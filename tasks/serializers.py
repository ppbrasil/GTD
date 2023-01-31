from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'name',
            'focus',
            'done',
            'due_date',
            'reminder',
            'readiness',
            'notes',
        ]