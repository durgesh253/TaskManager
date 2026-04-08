from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm, AssigneeStatusForm, AssignerDueDateForm
from accounts.models import User


def get_user_tasks(user):
    """Get all tasks visible to a user"""
    return Task.objects.filter(
        Q(created_by=user) | Q(assigned_to=user)
    ).select_related('created_by', 'assigned_to').distinct()


@login_required
def dashboard(request):
    user = request.user
    all_tasks = get_user_tasks(user)

    # Stats
    personal_tasks = all_tasks.filter(created_by=user, assigned_to=None)
    assigned_by_me = all_tasks.filter(created_by=user, assigned_to__isnull=False)
    assigned_to_me = all_tasks.filter(assigned_to=user)

    # Filters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    type_filter = request.GET.get('type', '')

    tasks = all_tasks
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if type_filter == 'personal':
        tasks = tasks.filter(created_by=user, assigned_to=None)
    elif type_filter == 'assigned_by_me':
        tasks = tasks.filter(created_by=user, assigned_to__isnull=False)
    elif type_filter == 'assigned_to_me':
        tasks = tasks.filter(assigned_to=user)

    context = {
        'tasks': tasks,
        'personal_count': personal_tasks.count(),
        'assigned_by_me_count': assigned_by_me.count(),
        'assigned_to_me_count': assigned_to_me.count(),
        'total_count': all_tasks.count(),
        'todo_count': all_tasks.filter(status='todo').count(),
        'in_progress_count': all_tasks.filter(status='in_progress').count(),
        'done_count': all_tasks.filter(status='done').count(),
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'type_filter': type_filter,
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    # Access control
    if task.created_by != user and task.assigned_to != user:
        messages.error(request, 'You do not have permission to view this task.')
        return redirect('dashboard')

    is_creator = task.created_by == user
    is_assignee = task.assigned_to == user

    context = {
        'task': task,
        'is_creator': is_creator,
        'is_assignee': is_assignee,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    is_creator = task.created_by == user
    is_assignee = task.assigned_to == user

    # Authorization
    if not is_creator and not is_assignee:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('dashboard')

    if request.method == 'POST':
        if is_creator and task.is_personal:
            # Personal task - full edit
            form = TaskForm(request.POST, instance=task, user=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task updated successfully!')
                return redirect('task_detail', pk=pk)
        elif is_creator and task.is_assigned:
            # Assigner: can update due_date only
            form = AssignerDueDateForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Due date updated successfully!')
                return redirect('task_detail', pk=pk)
        elif is_assignee:
            # Assignee: can only update status
            form = AssigneeStatusForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task status updated!')
                return redirect('task_detail', pk=pk)
        else:
            messages.error(request, 'Permission denied.')
            return redirect('dashboard')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    # GET - choose correct form
    if is_creator and task.is_personal:
        form = TaskForm(instance=task, user=user)
        form_type = 'full'
    elif is_creator and task.is_assigned:
        form = AssignerDueDateForm(instance=task)
        form_type = 'due_date'
    else:
        form = AssigneeStatusForm(instance=task)
        form_type = 'status_only'

    context = {
        'form': form,
        'task': task,
        'form_type': form_type,
        'is_creator': is_creator,
        'is_assignee': is_assignee,
        'action': 'Edit',
    }
    return render(request, 'tasks/task_edit.html', context)


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    if task.created_by != user:
        messages.error(request, 'Only the task creator can delete this task.')
        return redirect('dashboard')

    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('dashboard')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
