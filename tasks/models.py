"""
Task model for the multiuser TODO list.
"""

from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """A task assigned by a teacher, with due date and course."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    course = models.CharField(max_length=100, blank=True, help_text="e.g., 15-213, 21-127")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["due_date", "created_at"]

    def __str__(self):
        return f"{self.title} ({self.course or 'No course'})"
