from rest_framework import serializers

from .models import Task

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'name',
        ]

class WaitingForSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'person',
            'due_date',
        ]

class TaskSerializer(serializers.ModelSerializer):
    waiting_for = WaitingForSerializer(read_only=True)
    # tags = TagsSerializer(many=True)
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
            'tags',
        ]