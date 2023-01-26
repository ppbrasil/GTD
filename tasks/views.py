from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import TaskCreationForm, TaskFilterForm
from .models import Task
from django.db.models import Q
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

@login_required
def filtered_list_task(request):
    form = TaskFilterForm(request.GET or None)
    if form.is_valid():
        # Generate complet list for the user
        tasks = Task.objects.filter(user=request.user)
        for task in tasks:
            print(task.name)
            print(task.done)
            print(task.readiness)
            print(task.focus)
        # Present only complete or uncomplete
        if form.cleaned_data['done']==True:
            tasks = tasks.filter(done__exact=form.cleaned_data['done'])
        print(tasks)
        
        # Filter based on focus   
        if form.cleaned_data['focus']==True:
            tasks = tasks.filter(focus__exact=form.cleaned_data['focus'])
        print(tasks)
        
        # Filter readiness
        if form.cleaned_data['readiness']:
            if form.cleaned_data['readiness']!='empty':                
                tasks = tasks.filter(readiness__exact=form.cleaned_data['readiness'])
        print(tasks)
        return render(request, 'filtered_list_task.html', {'tasks': tasks, 'user': request.user, 'form': form})
    else:
        return render(request, 'filtered_list_task.html', {'user': request.user, 'form': form})

'''
@login_required
def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    context = {'task': task}
    return render(request, 'task_detail.html', context)
'''