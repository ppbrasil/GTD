from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class SimpleTag(Tag):
    pass

class Person(Tag):
    pass

class Place(Tag):
    pass

class Area(Tag):
    pass

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    focus = models.BooleanField(default=False)
    overdue = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    set_focus_date = models.DateField(null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    readiness = models.CharField(
        max_length=20,
        choices=[
            ('inbox', 'Inbox'),
            ('anytime', 'Anytime'),
            ('waiting', 'Waiting'),
            ('sometime', 'Sometime')
        ],
        default='inbox'
    )
    waiting_for_person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True, related_name='waiting_for_tasks')
    waiting_for_time = models.DateTimeField(null=True, blank=True)
    simpletags = models.ManyToManyField(SimpleTag, through='TaskSimpleTag', blank=True)
    persons = models.ManyToManyField(Person, through='TaskPerson', blank=True, related_name='tasks')
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskPerson(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class TaskSimpleTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    simpletag = models.ForeignKey(SimpleTag, on_delete=models.CASCADE)

