from django import forms
from .models import Task
from datetime import datetime

class TaskCreationForm(forms.ModelForm):
    reminder_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    reminder_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = Task
        fields = ['name', 'done', 'due_date', 'reminder', 'focus', 'readiness', 'waiting_for', 'tags', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),

            #hide reminder so user dont get two different way to input that info
            #reminder_date and reminder_time are being combined in the views funtion create_task()
            'reminder': forms.HiddenInput
        }


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
