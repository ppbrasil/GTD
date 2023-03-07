import warnings
from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

from .models import Task, SimpleTag, Person, Place


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

    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     simpletag_name = attrs.get('name')

    #     # Check if a SimpleTag with the same name already exists for the user
    #     if SimpleTag.objects.filter(user=user, name=simpletag_name).exists():
    #         raise serializers.ValidationError('A simpletag with this name already exists.')
        
    #     return attrs
    
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

    # def validate(self, attrs):
    #     user = self.context['request'].user
    #     person_name = attrs.get('name')

    #     # Check if a Place with the same name already exists for the user
    #     if Person.objects.filter(user=user, name=person_name).exists():
    #         raise serializers.ValidationError('A person with this name already exists.')
        
    #     return attrs
    
class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Place
        fields = [
            'id', 
            'name',
            'is_active',
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        place_name = attrs.get('name')

        # Check if a Place with the same name already exists for the user
        if Place.objects.filter(user=user, name=place_name).exists():
            raise serializers.ValidationError('A place with this name already exists.')
        
        return attrs

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    due_date = serializers.DateField(required=False, allow_null=True)
    reminder = serializers.DateTimeField(required=False, allow_null=True) 
    waiting_for_person = PersonSerializer(required=False, allow_null=True)
    waiting_for_time = serializers.DateTimeField(required=False, allow_null=True)
    simpletags = SimpleTagSerializer(many=True, required=False)
    persons = PersonSerializer(many=True, required=False)
    place = PlaceSerializer(required=False, allow_null=True)

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
            'waiting_for_person',
            'waiting_for_time',
            'notes',
            'simpletags',
            'persons',
            'place',
        ]

    def get_waiting_for_person(self, obj):
        waiting_for_person = getattr(obj, 'waiting_for_person', None)
        if waiting_for_person:
            return PersonSerializer(waiting_for_person).data
        else:
            return None

    def create(self, validated_data):
        simpletags_data = validated_data.pop('simpletags', [])
        persons_data = validated_data.pop('persons', [])
        place_data = validated_data.pop('place', None)
        waiting_for_person_data = validated_data.pop('waiting_for_person', None)
        waiting_for_time_data = validated_data.get('waiting_for_time', None)

        task = Task.objects.create(**validated_data)

        if waiting_for_person_data is not None:
            person, created = Person.objects.get_or_create(user=task.user, name=waiting_for_person_data['name'])
            task.waiting_for_person = person

        if waiting_for_time_data is not None:
            waiting_for_time_data = timezone.datetime.fromisoformat(str(waiting_for_time_data))
            task.waiting_for_time = waiting_for_time_data

        if place_data is not None:
            place, created = Place.objects.get_or_create(user=task.user, name=place_data['name'])
            task.place = place

        for simpletag_data in simpletags_data:
            simpletag, created = SimpleTag.objects.get_or_create(user=task.user, name=simpletag_data['name'])
            task.simpletags.add(simpletag)

        for person_data in persons_data:
            person, created = Person.objects.get_or_create(user=task.user, name=person_data['name'])
            task.persons.add(person)

        task.save()
        return task

    def update(self, instance, validated_data):
        simpletags_data = validated_data.pop('simpletags', None)
        persons_data = validated_data.pop('persons', None)
        waiting_for_person_data = validated_data.pop('waiting_for_person', None)
        waiting_for_time_data = validated_data.get('waiting_for_time', None)
        place_data = validated_data.pop('place', None)

        instance = super().update(instance, validated_data)
        
        if 'waiting_for_person' in self.context['request'].data:
            if waiting_for_person_data is not None:
                person, created = Person.objects.get_or_create(user=instance.user, name=waiting_for_person_data['name'])
            else:
                person = None
            instance.waiting_for_person = person

        if waiting_for_time_data is not None:
            instance.waiting_for_time = timezone.datetime.fromisoformat(str(waiting_for_time_data)).replace(tzinfo=timezone.utc)
        
        if 'place' in self.context['request'].data:
            if place_data is not None:
                place, created = Place.objects.get_or_create(user=instance.user, name=place_data['name'])
            else:
                place = None
            instance.place = place

        if simpletags_data is not None:
            instance.simpletags.clear()
            for simpletag_data in simpletags_data:
                simpletag, created = SimpleTag.objects.update_or_create(user=instance.user, name=simpletag_data['name'])
                instance.simpletags.add(simpletag)
      
        if persons_data is not None:
            instance.persons.clear()
            for person_data in persons_data:
                person, created = Person.objects.get_or_create(user=instance.user, name=person_data['name'])
                instance.persons.add(person)
        
        instance.save()
        return instance

