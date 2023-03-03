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

class WaitingFor(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, blank=True)
    waiting_date = models.DateTimeField(null=True, blank=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    done = models.BooleanField(default=False)
    focus = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
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
    waiting_for = models.ForeignKey(WaitingFor, on_delete=models.CASCADE, null=True, blank=True)
    simpletags = models.ManyToManyField(SimpleTag, through='TaskSimpleTag', blank=True)
    persons = models.ManyToManyField(Person, through='TaskPerson', blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TaskPerson(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class TaskSimpleTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    simpletag = models.ForeignKey(SimpleTag, on_delete=models.CASCADE)
