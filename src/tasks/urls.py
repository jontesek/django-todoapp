from django.urls import path

from . import views

urlpatterns = [
    # Health check
    path("health/", views.health),
    # Task list or create
    path("", views.TaskList.as_view()),
    # Task by ID
    path("<int:pk>/", views.TaskDetail.as_view()),
    # Tasks without parent
    path("root/", views.RootTaskList.as_view()),
    # Direct subtasks
    path('<int:pk>/subtasks/', views.SubtasksList.as_view()),
    # All subtasks
    path('<int:pk>/subtasks-tree/', views.SubtasksTreeList.as_view()),
]