from django import forms
from .models import Task

class TaskCreationForm(forms.ModelForm):
    reminder_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    reminder_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = Task
        fields = ['name', 'done', 'due_date', 'reminder', 'focus', 'readiness', 'waiting_for', 'tags', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'task-name'}),
            'done': forms.CheckboxInput(attrs={'class': 'done-checkbox'}),
            'focus': forms.CheckboxInput(attrs={'class': 'focus-checkbox'}),
            'notes': forms.Textarea(attrs={'class': 'notes-text', 'rows': '3'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%d-%m-%Y'),
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
