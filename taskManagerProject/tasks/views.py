from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def tasks(request):
    current = Task.objects.filter(user=request.user, completeDate__isnull = True)
    completed = Task.objects.filter(user=request.user, completeDate__isnull = False)
    return render(request, 'tasks.html', {'current':current, 'completed': completed})

@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form':TaskForm})
    else: #post
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'create.html', {'error': error, 'form':TaskForm})

@login_required  
def delete_task(request, taskId):
    task = get_object_or_404(Task, id=taskId, user=request.user)
    task.delete()
    return redirect('tasks')

@login_required
def detail(request, taskId):
    task = get_object_or_404(Task, id=taskId, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'detail.html', {'form':form, 'task':task})
    else: #POST
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'detail.html', {'error':error, 'form':form, 'task':task})

@login_required
def complete(request, taskId):
    task = get_object_or_404(Task, id=taskId, user=request.user)
    task.completeDate = timezone.now()
    task.save()
    return redirect('tasks')