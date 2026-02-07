"""
URL configuration for the core app.

Defines routes for the homepage, static pages, and any global endpoints
that do not belong to a specific feature app. This module also provides
a clean separation between project-level routing and app-level routing.
"""


from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    # Garden beds
    path("beds/", views.bed_list, name="bed_list"),
    path("beds/<int:pk>/", views.bed_detail, name="bed_detail"),

    path("", views.home, name="home"),
]
