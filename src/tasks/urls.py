from django.urls import path

from . import views

urlpatterns = [
    # Health check
    path("health/", views.health),
    # List tasks, create new task
    path("", views.TaskList.as_view(), name="tasks-all"),
    # Task by ID
    path("<int:pk>/", views.TaskDetail.as_view(), name="task-detail"),
    # Tasks without parent
    path("root/", views.RootTaskList.as_view(), name="only-root-tasks"),
    # Direct subtasks
    path("<int:pk>/subtasks/", views.SubtasksList.as_view(), name="direct-subtasks"),
    # All subtasks
    path("<int:pk>/subtasks-tree/", views.SubtasksTreeList.as_view(), name="subtasks-tree"),
]
