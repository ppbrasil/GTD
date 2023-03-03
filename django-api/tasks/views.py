# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .forms import TaskCreationForm, TaskFilterForm
# from .models import Task
# from datetime import date, datetime
# ## from models import Task

# @login_required
# def create_task(request):
#     if request.method == 'POST':
#         form = TaskCreationForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             reminder_date = form.cleaned_data.get('reminder_date')
#             reminder_time = form.cleaned_data.get('reminder_time')
#             task.reminder = datetime.combine(reminder_date, reminder_time)
#             task.user = request.user
#             task.save()
#     else:
#         form = TaskCreationForm(initial={'user':request.user})
#     return render(request, 'dashboard.html', {'form': form})

# @login_required
# def list_task(request):
#     list_user = request.user
#     tasks = Task.objects.filter(user=list_user)
#     return render(request, 'list_task.html', {'tasks': tasks, 'user': list_user})

# @login_required
# def filtered_list_task(request):
#     form = TaskFilterForm(request.GET or None)
#     if form.is_valid():
#         # Generate complet list for the user
#         tasks = Task.objects.filter(user=request.user)
#         for task in tasks:
#             print(task.name)
#             print(task.reminder)
#         # Present only complete or uncomplete
#         if form.cleaned_data['done']==True:
#             tasks = tasks.filter(done__exact=form.cleaned_data['done'])
        
#         # Filter based on focus   
#         if form.cleaned_data['focus']==True:
#             tasks = tasks.filter(focus__exact=form.cleaned_data['focus'])
        
#         # Filter readiness
#         if form.cleaned_data['readiness']:
#             if form.cleaned_data['readiness']!='empty':                
#                 tasks = tasks.filter(readiness__exact=form.cleaned_data['readiness'])

#         return render(request, 'filtered_list_task.html', {'tasks': tasks, 'user': request.user, 'form': form})
#     else:
#         return render(request, 'filtered_list_task.html', {'user': request.user, 'form': form})

# # filtered Inbox
# @login_required
# def readiness_filter(request, filter):
#     filtered_tasks = Task.objects.filter(readiness=filter, done=False)
#     form = TaskCreationForm(initial={'user':request.user})
#     return render(request, 'dashboard.html', {'tasks': filtered_tasks, 'form':form})

# # filtered Focus
# @login_required
# def focus_filter(request):
#     filtered_tasks = Task.objects.filter(focus=True, done=False)
#     form = TaskCreationForm(initial={'user':request.user})
#     return render(request, 'dashboard.html', {'tasks': filtered_tasks, 'form':form})

# # filtered Done
# @login_required
# def done_filter(request):
#     filtered_tasks = Task.objects.filter(done=True)
#     form = TaskCreationForm(initial={'user':request.user})
#     return render(request, 'dashboard.html', {'tasks': filtered_tasks, 'form':form})


# '''
# @login_required
# def task_detail(request, pk):
#     task = Task.objects.get(pk=pk)
#     context = {'task': task}
#     return render(request, 'task_detail.html', context)
# '''