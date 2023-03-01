import warnings
from django.utils import timezone
from rest_framework import serializers

from .models import Task
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = [
            'id', 
            'name'
        ]

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    tags = TagSerializer(many=True, required=False)
    due_date = serializers.DateField(required=False, allow_null=True)
    reminder = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'focus',
            'done',
            'due_date',
            'reminder',
            'readiness',
            'notes',
            'tags',
        ]

    def get_tags(self, obj):
        return TagSerializer(obj.tags.all(), many=True).data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=task.user, name=tag_data['name'])
            task.tags.add(tag)
        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(user=instance.user, name=tag_data['name'])
                instance.tags.add(tag)
        return instance

