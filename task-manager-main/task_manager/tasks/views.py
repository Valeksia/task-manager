from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import ToDo


@login_required
def index(request):
    todos = ToDo.objects.filter(user=request.user)  # Фильтрация задач по текущему пользователю
    return render(request, 'tasks/index.html', {'todo_list': todos, 'title': 'Главная страница'})


@login_required
@require_http_methods(['POST'])
def add(request):
    title = request.POST['title']
    deadline = request.POST.get('deadline')
    priority = request.POST.get('priority')

    # Создание задачи для текущего пользователя
    todo = ToDo(user=request.user, title=title, deadline=deadline, priority=priority)
    todo.save()

    return redirect('tasks:index')


@login_required
def update(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)

    if todo.user == request.user:
        todo.is_complete = not todo.is_complete
        todo.save()

    return redirect('tasks:index')


@login_required
@require_http_methods(['POST'])
def delete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)

    if todo.user == request.user:
        todo.delete()

    return redirect('tasks:index')


@login_required
@require_http_methods(['POST'])
def edit(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)

    if todo.user == request.user:
        todo.title = request.POST['title']

        deadline = request.POST.get('deadline')
        if deadline:
            todo.deadline = deadline

        priority = request.POST.get('priority')
        if priority:
            todo.priority = priority

        todo.save()

    return redirect('tasks:index')