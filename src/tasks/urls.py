from django.urls import path

from . import views

urlpatterns = [
    # Health check
    path("health/", views.health, name="Health check"),
]