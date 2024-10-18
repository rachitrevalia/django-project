from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import createuserform, LoginForm, CreateTask
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Task, AssignTask
from .forms import AssignTaskForm, FeedbackForm
from django.views import View
from django.contrib import messages

# Create your views here.

def home(request):
    """Render the homepage."""
    return render(request, 'index.html')

def about(request):
    """Render the about page."""
    return render(request, 'about.html')

def info1(request):
    """Render the info1 page."""
    return render(request, 'info1.html')

def info2(request):
    """Render the info2 page."""
    return render(request, 'info2.html')

def logout(request):
    """Render the logout page."""
    return render(request, 'logout.html')

def register(request):
    """Handle user registration."""
    form = createuserform()
    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect("my-login")  # Redirect to login page

    context = {'form': form}
    return render(request, 'register.html', context=context)

def my_login(request):
    """Handle user login."""
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)  # Log the user in
                return redirect("dashboard")  # Redirect to dashboard

    context = {'form': form}
    return render(request, 'my-login.html', context=context)

@login_required(login_url='my-login')
def dashboard(request):
    """Render the user dashboard with tasks assigned to the current user."""
    currentuser = request.user.id
    task = Task.objects.filter(user=currentuser)  # Get tasks for the current user
    username = request.user.username
    context = {'task': task, 'username': username}
    return render(request, 'profile/dashboard.html', context=context)

def user_logout(request):
    """Logout the user and redirect to the homepage."""
    auth.logout(request)
    return redirect("")  # Redirect to homepage

@login_required(login_url='my-login')
def createTask(request):
    """Handle task creation."""
    form = CreateTask()
    if request.method == 'POST':
        form = CreateTask(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Create a task instance without saving
            task.user = request.user  # Associate task with the logged-in user
            task.save()  # Save the task
            return redirect('dashboard')  # Redirect to dashboard

    context = {'form': form}
    return render(request, 'profile/create-task.html', context=context)

@login_required(login_url='my-login')
def updateTask(request, pk):
    """Handle updating an existing task."""
    task = Task.objects.get(id=pk)  # Get the task by ID
    form = CreateTask(instance=task)
    if request.method == 'POST':
        form = CreateTask(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Save the updated task
            return redirect('dashboard')  # Redirect to dashboard

    context = {'form': form}
    return render(request, 'profile/update-task.html', context=context)

@login_required(login_url='my-login')
def deleteTask(request, pk):
    """Handle task deletion."""
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()  # Delete the task
        return redirect('dashboard')  # Redirect to dashboard

    return render(request, 'profile/delete-task.html')

@login_required(login_url='my-login')
def assignTask(request):
    """Handle assigning a task to another user."""
    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            assigned_task = form.save(commit=False)
            assigned_task.user = request.user  # Associate with the logged-in user
            assigned_task.save()  # Save the assigned task
            return redirect('assign-dashboard')
    else:
        form = AssignTaskForm()  # Create a new form instance if not POST
    context = {'form': form}
    return render(request, 'profile/assign-task.html', context=context)

@login_required(login_url='my-login')
def assignDashboard(request):
    """Render a dashboard for tasks assigned to and by the current user."""
    current_user = request.user
    assigned_tasks = AssignTask.objects.filter(assigned_to=current_user)  # Tasks assigned to the user
    tasks_assigned_to_me = AssignTask.objects.filter(assigned_by=current_user)  # Tasks assigned by the user
    context = {
        'assigned_task': tasks_assigned_to_me,
        'task_assigned_to_me': assigned_tasks,
    }
    return render(request, 'profile/assign-dashboard.html', context=context)

@login_required(login_url='my-login')
def updateassignedTask(request, pk):
    """Handle updating an assigned task."""
    task = AssignTask.objects.get(id=pk)
    form = AssignTaskForm(instance=task)
    if request.method == 'POST':
        form = AssignTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Save the updated assigned task
            return redirect('assign-dashboard')
    context = {'form': form}
    return render(request, 'profile/update-assigned-task.html', context=context)

@login_required(login_url='my-login')
def deleteassignedTask(request, pk):
    """Handle deleting an assigned task."""
    task = AssignTask.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()  # Delete the assigned task
        return redirect('assign-dashboard')

    return render(request, 'profile/delete-assigned-task.html')

@login_required(login_url='my-login')
def completedTask(request, pk):
    """Handle marking a task as completed (delete in this case)."""
    task = AssignTask.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()  # Delete the task to mark as completed
        return redirect('assign-dashboard')

    return render(request, 'profile/completed-task.html')

class TaskSearchView(View):
    """View to handle searching for tasks."""
    def get(self, request):
        query = request.GET.get('q')  # Get the search query from request
        tasks = Task.objects.filter(title__icontains=query)  # Filter tasks by title
        return render(request, 'task-search.html', {'tasks': tasks, 'query': query})

def submit_feedback(request):
    """Handle user feedback submission."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save the feedback
            messages.success(request, 'Thank you for your feedback!')  # Show success message
            return redirect('submit-feedback')  # Redirect to feedback page
    else:
        form = FeedbackForm()  # Create a new form instance if not POST

    return render(request, 'feedback-form.html', {'form': form})