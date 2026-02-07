"""
Views for the core app, including homepage rendering, custom error handlers,
and any shared view logic used across the project.

These views provide the entry point to the application and support global
behaviours that are not tied to a specific feature area such as plants,
tasks, or user accounts.
"""


from django.shortcuts import render


def home(request):
    """
    Render the public homepage for the Garden Timekeeper application.

    This view introduces the app and provides navigation to registration
    and login pages. It is accessible to both authenticated and anonymous
    users.
    """
    return render(request, 'core/home.html')
