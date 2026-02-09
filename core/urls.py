"""
URL configuration for the core app.

Defines routes for the homepage, static pages, and any global endpoints
that do not belong to a specific feature app. This module also provides
a clean separation between project-level routing and app-level routing.
"""


from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Garden beds
    path("beds/", views.bed_list, name="bed_list"),
    path("beds/create/", views.bed_create, name="bed_create"),
    path("beds/<int:pk>/", views.bed_detail, name="bed_detail"),
    path("beds/<int:pk>/edit/", views.bed_edit, name="bed_edit"),
    path("beds/<int:pk>/delete/", views.bed_delete, name="bed_delete"),
]
