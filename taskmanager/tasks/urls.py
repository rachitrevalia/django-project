from django.urls import path
from . import views
from .views import TaskSearchView

urlpatterns = [
    path('', views.home, name=""),  # Home page
    path('register', views.register, name="register"),  # User registration page
    path('about', views.about, name="about"),  # About page
    path('info1', views.info1, name="info1"),  # Info page 1
    path('info2', views.info2, name="info2"),  # Info page 2
    path('my-login', views.my_login, name="my-login"),  # User login page
    path('dashboard', views.dashboard, name="dashboard"),  # User dashboard
    path('user-logout', views.user_logout, name="user-logout"),  # Logout user
    path('logout', views.logout, name="logout"),  # Logout page
    path('create-task', views.createTask, name="create-task"),  # Create a new task
    path('update-task/<str:pk>/', views.updateTask, name="update-task"),  # Update a task by its ID
    path('delete-task/<str:pk>/', views.deleteTask, name="delete-task"),  # Delete a task by its ID
    path('assign-task/', views.assignTask, name='assign-task'),  # Assign a task to another user
    path('assign-dashboard/', views.assignDashboard, name='assign-dashboard'),  # Dashboard for assigned tasks
    path('update-assigned-task/<str:pk>/', views.updateassignedTask, name="update-assigned-task"),  # Update an assigned task
    path('delete-assigned-task/<str:pk>/', views.deleteassignedTask, name="delete-assigned-task"),  # Delete an assigned task
    path('completed-task/<str:pk>/', views.completedTask, name="completed-task"),  # Mark an assigned task as completed
    path('search/', TaskSearchView.as_view(), name='task-search'),  # Search for tasks
    path('feedback/', views.submit_feedback, name='submit-feedback'),  # Submit feedback
]