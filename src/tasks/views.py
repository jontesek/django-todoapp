from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import TaskSerializer
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
        return Task.objects.filter(user=self.request.user, parent=task_id)
