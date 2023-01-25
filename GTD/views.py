from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from tasks.models import Task
from tasks.forms import TaskCreationForm


@login_required
def dashboard(request):
   CreationForm = TaskCreationForm()
   tasks = Task.objects.all()
   return render(request, 'dashboard.html', {'form': CreationForm, 'tasks': tasks})
   