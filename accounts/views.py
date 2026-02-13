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
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm


def login_view(request):
    """
    Handle user login using the custom LoginForm.

    Workflow:
    - GET request: display a blank login form
    - POST request:
        * Bind submitted data to LoginForm
        * Validate credentials using Django's authentication backend
        * On success:
           - log the user in,
           -  apply remember-me logic,
           -  redirect to dashboard
        * On failure: re-render the form with field-level and general errors

    The LoginForm handles:
    - Username/password validation
    - Bootstrap styling via __init__
    - Field-level error messages

    The view focuses solely on flow control and user feedback.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            remember_me = request.POST.get("remember_me")

            login(request, user)

            # Session expiry logic
            if not remember_me:
                request.session.set_expiry(0)  # Ends when browser closes
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            messages.success(request, f"Welcome back {user.username}!")
            return redirect("dashboard")

        messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    """
    Log the user out of their account.

    Ends the user's authenticated session, displays a confirmation
    message, and redirects them to the login page.

    This view performs no validation or form handling — it simply
    terminates the session and provides user feedback.
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
