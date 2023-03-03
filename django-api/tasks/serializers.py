import warnings
from django.utils import timezone
from rest_framework import serializers

from .models import Task, SimpleTag, Person


class SimpleTagSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = SimpleTag
        fields = [
            'id', 
            'name',
            'is_active',
        ]

class PersonSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Person
        fields = [
            'id', 
            'name',
            'is_active',
        ]
class TaskSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    simpletags = SimpleTagSerializer(many=True, required=False)
    persons = PersonSerializer(many=True, required=False)
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
            'simpletags',
            'persons',
        ]

    def get_tags(self, obj):
        return SimpleTagSerializer(obj.simpletags.all(), many=True).data

    def create(self, validated_data):
        simpletags_data = validated_data.pop('simpletags', [])
        task = Task.objects.create(**validated_data)
        for simpletag_data in simpletags_data:
            simpletag, created = SimpleTag.objects.get_or_create(user=task.user, name=simpletag_data['name'])
            task.simpletags.add(simpletag)
        return task

    def update(self, instance, validated_data):
        simpletags_data = validated_data.pop('simpletags', None)
        instance = super().update(instance, validated_data)
        if simpletags_data is not None:
            instance.simpletags.clear()
            for simpletag_data in simpletags_data:
                simpletag, created = SimpleTag.objects.update_or_create(user=instance.user, name=simpletag_data['name'])
                instance.simpletags.add(simpletag)
        return instance

