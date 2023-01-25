from django import forms
from .models import Task

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'reminder', 'focus', 'readiness', 'waiting_for', 'tags', 'notes']
