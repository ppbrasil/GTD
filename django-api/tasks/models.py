from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class People(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class WaitingFor(models.Model):
    person = models.ForeignKey(People, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)

class Tag(models.Model):
    name = models.CharField(max_length=255)
        
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

    readiness = models.CharField(max_length=20, choices=[
        ('inbox', 'Inbox'), ('anytime', 'Anytime'), ('waiting', 'Waiting'), ('sometime', 'Sometime')
        ], default='inbox')
    waiting_for = models.ForeignKey(WaitingFor, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



