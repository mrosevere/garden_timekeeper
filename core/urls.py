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
    bed_delete,  # function-based delete view
)

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Garden beds (CBVs)
    path("beds/", BedListView.as_view(), name="bed_list"),
    path("beds/<int:pk>/", BedDetailView.as_view(), name="bed_detail"),
    path("beds/create/", BedCreateView.as_view(), name="bed_create"),
    path("beds/<int:pk>/edit/", BedUpdateView.as_view(), name="bed_edit"),

    # Garden bed delete (FBV for modal workflow)
    path("beds/<int:pk>/delete/", bed_delete, name="bed_delete"),
]
