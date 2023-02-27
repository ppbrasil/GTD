import warnings
from django.utils import timezone
from rest_framework import serializers

from .models import Task
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

    def update(self, instance, validated_data):
        if not instance.is_active:
            raise serializers.ValidationError('Cannot update inactive Tag object')
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

# class TagsSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = [
#             'name',
#         ]

class WaitingForSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'person',
            'due_date',
        ]

class TaskSerializer(serializers.ModelSerializer):
    waiting_for = WaitingForSerializer(read_only=True)
    due_date = serializers.DateField(required=False, allow_null=True)
    reminder = serializers.DateTimeField(required=False, allow_null=True)

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

        def update(self, instance, validated_data):
            if not instance.is_active:
                raise serializers.ValidationError('Cannot update inactive Task object')
            instance.name = validated_data.get('name', instance.name)
            instance.focus = validated_data.get('focus', instance.focus)
            instance.done = validated_data.get('done', instance.done)
            instance.waiting_for = validated_data.get('waiting_for', instance.waiting_for)
            instance.due_date = validated_data.get('due_date', instance.due_date)
            instance.reminder = validated_data.get('reminder', instance.reminder)
            instance.readiness = validated_data.get('readiness', instance.readiness)
            instance.notes = validated_data.get('notes', instance.notes)
            instance.save()
            return instance