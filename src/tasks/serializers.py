from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "is_completed", "parent", "created_at", "updated_at"]

    def validate_parent(self, value):
        request = self.context.get('request')

        # Check that only user's task can be set as parent
        if value and request and value.user != request.user:
            raise serializers.ValidationError("Unauthorized parent task.")

        # Check if the task's parent is itself OR any of its own subtasks (preventing loops)
        if self.instance and value:
            # If the new parent is currently a child of this task, it's a loop!
            curr = value
            while curr is not None:
                if curr.pk == self.instance.pk:
                    raise serializers.ValidationError("Circular dependency detected.")
                curr = curr.parent
        return value
