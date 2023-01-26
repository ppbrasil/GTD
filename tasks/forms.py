from django import forms
from .models import Task
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'done', 'due_date', 'reminder', 'focus', 'readiness', 'waiting_for', 'tags', 'notes']


class TaskFilterForm(forms.Form):
    done = forms.BooleanField(required=False)
    readiness = forms.ChoiceField(choices=[
        ('empty', '---'),
        ('inbox', 'inbox'),
        ('anytime', 'Anytime'),
        ('waiting', 'Waiting'),
        ('sometime', 'Sometime')
    ], required=False)
    focus = forms.BooleanField(required=False)
