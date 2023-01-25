from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskCreationForm
from .models import Task
## from models import Task

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
    else:
        form = TaskCreationForm(initial={'user':request.user})
    return render(request, 'dashboard.html', {'form': form})

@login_required
def list_task(request):
    list_user = request.user
    tasks = Task.objects.filter(user=list_user)
    return render(request, 'list_task.html', {'tasks': tasks, 'user': list_user})


'''
@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    context = {'task': task}
    return render(request, 'task_detail.html', context)
'''