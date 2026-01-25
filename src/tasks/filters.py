from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['icontains', 'exact'],
            'description': ['icontains', 'exact'],
            'due_date': ['gt', 'lt', 'gte', 'lte', 'exact', 'isnull'],
            'is_completed': ['exact'],
            'parent': ['exact', 'isnull'],
            'created_at': ['gt', 'lt'],
            'updated_at': ['gt', 'lt'],
        }