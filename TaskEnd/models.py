from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
class Task(models.Model):
    priority_choices = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=priority_choices,
        default="medium"
    )

    owner = models.ForeignKey(
        User, 
        on_delete = models.CASCADE
    )
def __str__(self):
    return self.title
def get_status(self):
    if self.completed:
        return "done"
    if self.deadline and self.deadline < now():
        return "overdue"
    if self.deadline:
        return "pending"
    return "no-deadline, enjoy hard!"