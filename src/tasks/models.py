from django.db import models


class Task(models.Model):
    # Basic attributes
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    # Relationships
    parent = models.ForeignKey("Task", related_name="subtasks", on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey("auth.User", related_name="tasks", on_delete=models.CASCADE)
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
