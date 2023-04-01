import warnings
from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

from .models import Task, SimpleTag, Person, Place, Area, Project


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

class AreaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Area
        fields = [
            'id', 
            'name',
            'is_active',
        ]
    
class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    is_active = serializers.BooleanField(default=True)
    area = AreaSerializer(required=False, allow_null=True)

    class Meta:
        model = Project
        fields = [
            'id', 
            'name',
            'area',
            'is_active',
        ]

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    due_date = serializers.DateField(required=False, allow_null=True)
    reminder = serializers.DateTimeField(required=False, allow_null=True) 
    waiting_for_person = PersonSerializer(required=False, allow_null=True)
    waiting_for_time = serializers.DateTimeField(required=False, allow_null=True)
    simpletags = SimpleTagSerializer(many=True, required=False)
    persons = PersonSerializer(many=True, required=False)
    place = PlaceSerializer(required=False, allow_null=True)
    area = AreaSerializer(required=False, allow_null=True)
    project = ProjectSerializer(required=False, allow_null=True)

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
            'area',
            'project',
        ]

    def create(self, validated_data):
        simpletags_data = validated_data.pop('simpletags', [])
        persons_data = validated_data.pop('persons', [])
        place_data = validated_data.pop('place', None)
        waiting_for_person_data = validated_data.pop('waiting_for_person', None)
        waiting_for_time_data = validated_data.get('waiting_for_time', None)
        area_data = validated_data.pop('area', None)
        project_data = validated_data.pop('project', None)

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

        if project_data is not None:
            project, created = Project.objects.get_or_create(user=task.user, name=project_data['name'])
            task.project = project
            task.area = project.area
        
        elif area_data is not None:
            area, created = Area.objects.get_or_create(user=task.user, name=area_data['name'])
            task.area = area

        task.save()
        return task

    def update(self, instance, validated_data):

        if 'name' not in validated_data:
            validated_data['name'] = getattr(instance, 'name')
        if 'done' not in validated_data:
            validated_data['done'] = getattr(instance, 'done')
        if 'readiness' not in validated_data:
            validated_data['readiness'] = getattr(instance, 'readiness')

        simpletags_data = validated_data.pop('simpletags', None)
        persons_data = validated_data.pop('persons', None)
        waiting_for_person_data = validated_data.pop('waiting_for_person', None)
        waiting_for_time_data = validated_data.get('waiting_for_time', None)
        place_data = validated_data.pop('place', None)
        area_data = validated_data.pop('area', None)
        project_data = validated_data.pop('project', None)

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
        
        if 'area' in self.context['request'].data:
            if area_data is not None:
                area, created = Area.objects.get_or_create(user=instance.user, name=area_data['name'])
            else:
                area = None
            instance.area = area

        if 'project' in self.context['request'].data:
            if project_data is not None:
                project, created = Project.objects.get_or_create(user=instance.user, name=project_data['name'])
            else:
                project = None
            instance.project = project

        instance.save()
        return instance

'''
Serializers to handle the task tree
'''
class TaskTreeSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Area
        fields = ('id', 'name', 'projects')

    def get_projects(self, obj):
        projects = obj.projects.filter(is_active=True)
        serializer = ProjectTreeSerializer(projects, many=True)
        return serializer.data

class ProjectTreeSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'tasks')

    def get_tasks(self, obj):
        tasks = obj.tasks.filter(done=False)
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data

class TaskTreeSerializer(serializers.ModelSerializer):
    simpletags = SimpleTagSerializer(many=True, required=False)
    persons = PersonSerializer(many=True, required=False)
    place = PlaceSerializer(required=False, allow_null=True)
    project = ProjectSerializer(required=False, allow_null=True)
    area = AreaSerializer(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'simpletags', 'persons', 'place', 'project', 'area')
