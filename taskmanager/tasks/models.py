from django.db import models
from django.contrib.auth.models import User

# Model representing a task that users can create and manage
class Task(models.Model):
    title = models.CharField(max_length=100, null=True)  # Title of the task
    content = models.CharField(max_length=1000, null=True, blank=False)  # Detailed description of the task
    deadline = models.DateField(null=True, blank=True)  # Deadline for task completion
    date_posted = models.DateTimeField(auto_now_add=True, null=True)  # Timestamp for when the task was created
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)  # User who created the task

# Model representing an assigned task to another user
class AssignTask(models.Model):
    title = models.CharField(max_length=100, null=True)  # Title of the assigned task
    content = models.CharField(max_length=1000, null=True, blank=False)  # Detailed description of the assigned task
    deadline = models.DateField(null=True, blank=True)  # Deadline for the assigned task
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE)  # User to whom the task is assigned
    assigned_by = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.CASCADE, null=True)  # User who assigned the task
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)  # Timestamp for when the task was assigned

# Model for capturing user feedback
class Feedback(models.Model):
    name = models.CharField(max_length=100)  # Name of the user providing feedback
    email = models.EmailField()  # Email of the user providing feedback
    feedback = models.TextField()  # Content of the feedback
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the feedback was submitted

    def __str__(self):
        return f'Feedback from {self.name} - {self.email}'  # String representation of the Feedback object