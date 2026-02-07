"""
Views for user authentication and account management.

Includes:
- User login
- User logout
- User registration
- Any future account-related flows

These views provide the entry points for users to access and manage
their Garden Timekeeper accounts.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm


def login_view(request):
    """
    Handle user login.

    Workflow:
    - GET request: display the login form
    - POST request:
        * Extract username and password
        * Authenticate using Django's built-in system
        * On success: log the user in and redirect to home
        * On failure: re-render the login page with an error message

    This view does not use a Django form class because the login
    process is simple and handled by Django's authentication backend.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                # Session ends when browser closes
                request.session.set_expiry(0)
            else:
                # 2 weeks (Django default)
                request.session.set_expiry(1209600)
            messages.success(request, "Welcome back!")
            return redirect("dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


def logout_view(request):
    """
    Log the user out of their account.

    Ends the user's authenticated session, displays a confirmation
    message, and redirects them to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


def register_view(request):
    """
    Handle user registration using the custom RegistrationForm.

    Workflow:
    - GET request: display a blank registration form
    - POST request:
        * Bind submitted data to the form
        * Validate using Django's built-in and custom rules
        * On success: create the user, log them in, redirect to home
        * On failure: render form with field errors and a general msg

    The RegistrationForm handles:
    - Duplicate username validation
    - Password mismatch validation
    - Required field validation
    - Email validation
    - Bootstrap styling via __init__

    The view only manages flow control and user feedback.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")

        # Form is invalid — custom messages are already handled by the form
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
