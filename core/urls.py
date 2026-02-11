"""
URL configuration for the core app.

Defines routes for the homepage, dashboard, and garden bed management.
This module cleanly separates app-level routing from project-level routing.
"""

from django.urls import path
from . import views
from .views import (
    BedListView,
    BedDetailView,
    BedCreateView,
    BedUpdateView,
    bed_delete,
    PlantListView,
    PlantDetailView,
    PlantCreateView,
    PlantUpdateView,
    plant_delete,
    task_create,
    task_update,
    task_mark_done,
    task_skip
)

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Garden beds (Class Based Views)
    path("beds/", BedListView.as_view(), name="bed_list"),
    path("beds/<int:pk>/", BedDetailView.as_view(), name="bed_detail"),
    path("beds/create/", BedCreateView.as_view(), name="bed_create"),
    path("beds/<int:pk>/edit/", BedUpdateView.as_view(), name="bed_edit"),
    path("beds/<int:pk>/delete/", bed_delete, name="bed_delete"),

    # Garden bed delete (Function based views due to modal workflow)
    path("plants/",
         PlantListView.as_view(), name="plant_list"),
    path("plants/create/",
         PlantCreateView.as_view(), name="plant_create"),
    path("plants/<int:pk>/",
         PlantDetailView.as_view(), name="plant_detail"),
    path("plants/<int:pk>/edit/",
         PlantUpdateView.as_view(), name="plant_edit"),
    path("plants/<int:pk>/delete/",
         plant_delete, name="plant_delete"),

    # Tasks (Function based views)
    path("plants/<int:plant_id>/tasks/create/",
         task_create, name="task_create"),
    path("tasks/<int:task_id>/edit/",
         task_update, name="task_update"),
    path("tasks/<int:task_id>/done/",
         task_mark_done, name="task_mark_done"),
    path("tasks/<int:task_id>/skip/",
         task_skip, name="task_skip"),
]
