from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.core.paginator import Paginator

from todolist_app.models import TaskList
from todolist_app.form import TaskForm

from django.contrib.auth.decorators import login_required



# Create your views here.

# ver 1
# def todolist(request):
#    return HttpResponse("Welcome to Task Page")

# ver 2
# def todolist(request):
#   return render(request, 'todolist.html', {'welcome_text': "Welcome to Todo List App."})
    
# ver 3
# def todolist(request):
#    context = {
#        'welcome_text': "Welcome to Todo List Page."
#    }
#    return render(request, 'todolist.html', context)

# ver 4
@login_required
def todolist(request):

    if request.method == "POST":
        form = TaskForm(request.POST or None) 
        # None - if the field is empty
        
        if form.is_valid():
            #form.save(commit=False).manage = request.user
            #form.save()
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
            
        messages.success(request, ("New Task Added"))
        return redirect('todolist')

    else:

        # all_tasks = TaskList.objects.all
        # all_tasks - instance
        
        # return render(request, 'todolist.html', {'all_tasks': all_tasks})
        # this will display a queryset

        #all_tasks = TaskList.objects.all().order_by('id')
        all_tasks = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(all_tasks, 15)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {'all_tasks': all_tasks})

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request, ("Access Restricted"))
    return redirect('todolist')
    
@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task) 
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Edited"))
        return redirect('todolist')

    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True 
        task.save()
    else:
        messages.error(request, ("Access Restricted"))
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')

def contact(request):
    context = {
        'contact_text': "Welcome to Contact Page."
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'about_text': "Welcome to About Page."
    }
    return render(request, 'about.html', context)

def index(request):
    context = {
        'index_text': "Welcome to Index Page."
    }
    return render(request, 'index.html', context)


      