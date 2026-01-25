from collections import defaultdict

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import TaskSerializer, TaskTreeSerializer
from .models import Task
from .permissions import IsOwner


@api_view(['GET'])
def health(request):
    """Health check"""
    data = {"status": "ok"}
    return Response(data) 


class TaskList(generics.ListCreateAPIView):
    """List all tasks, create new task."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """Get task by ID, update values, delete task."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


class RootTaskList(generics.ListAPIView):
    """List all tasks without parent"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, parent=None)
    

class SubtasksList(generics.ListAPIView):
    """List all direct subtasks of the given task"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        task_id = self.kwargs.get('pk')
        get_object_or_404(Task, pk=task_id, user=self.request.user)
        return Task.objects.filter(user=self.request.user, parent=task_id)
    

class SubtasksTreeList(generics.ListAPIView):
    """List all subtasks of the given task in a hierarchical tree structure."""
    serializer_class = TaskTreeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    # Disable pagination to make sure the whole tree is returned
    pagination_class = None

    def get_queryset(self):
        # Get task ID from the URL
        task_id = self.kwargs.get('pk')

        # Check the task exists and is accessible by the user
        get_object_or_404(Task, pk=task_id, user=self.request.user)

        # Return only the direct children to start the list
        return Task.objects.filter(parent_id=task_id, user=self.request.user)

    def get_serializer_context(self):
        # Get all user tasks
        user_tasks = Task.objects.filter(user=self.request.user).only('id', 'parent_id')
        
        # Build a mapping of parent_id -> list of children
        children_map = defaultdict(list)
        for task in user_tasks:
            children_map[task.parent_id].append(task) # type: ignore
        
        # Put the map in context so the serializer can use it without queries
        context = super().get_serializer_context()
        context['children_map'] = children_map
        return context
