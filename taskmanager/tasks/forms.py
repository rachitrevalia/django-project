from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import Task, AssignTask, Feedback

# User creation form for registering new users
class createuserform(UserCreationForm):
    class Meta:
        model = User  # Specifies the User model
        fields = ['username', 'email', 'password1', 'password2']  # Fields to include in the form

# Login form for user authentication
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())  # Custom widget for username input
    password = forms.CharField(widget=PasswordInput())  # Custom widget for password input

# Form for creating new tasks
class CreateTask(forms.ModelForm):
    class Meta:
        model = Task  # Specifies the Task model
        fields = ['title', 'content', 'deadline']  # Fields to include in the form
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  # Custom widget for date input
        }
        # 'user' field is excluded, as it should be set programmatically

# Form for assigning tasks to other users
class AssignTaskForm(forms.ModelForm):
    class Meta:
        model = AssignTask  # Specifies the AssignTask model
        fields = ['title', 'content', 'deadline', 'assigned_to', 'assigned_by']  # Fields to include in the form
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),  # Custom widget for date input
            'assigned_to': forms.Select(),  # Dropdown for selecting user to assign task to
        }

# Form for submitting feedback
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback  # Specifies the Feedback model
        fields = ['name', 'email', 'feedback']  # Fields to include in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),  # Input for name
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),  # Input for email
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Feedback'}),  # Textarea for feedback
        }