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
    path('', views.home, name='home'),
]
