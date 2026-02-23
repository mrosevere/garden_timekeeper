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
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, AccountUpdateForm


def login_view(request):
    """
    Handle user login using the custom LoginForm.

    Workflow:
    - GET request:
        → Display a blank login form.
    - POST request:
        → Bind submitted data to LoginForm.
        → Validate credentials using Django's authentication backend.
        → On success:
              * Log the user in.
              * Apply 'Remember me' session‑expiry logic.
              * Redirect to the home page.
        → On failure:
              * Re-render the form with field-level and general errors.

    Notes:
    - The LoginForm handles:
        * Username/password validation.
        * Bootstrap styling via __init__.
        * Field-level error messages.
    - This view focuses solely on flow control and user feedback.
    """
    # print(">>> USING CUSTOM LOGIN_VIEW <<<")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            remember_me = request.POST.get("remember_me")

            # Log the user in
            login(request, user)

            # -----------------------------
            # Session expiry logic
            # -----------------------------
            # If 'Remember me' is NOT ticked:
            #   → Session expires when the browser closes.
            # If 'Remember me' IS ticked:
            #   → Session persists for 2 weeks (1209600 seconds).
            if not remember_me:
                request.session.set_expiry(0)  # Browser-session cookie
            else:
                request.session.set_expiry(1209600)  # 14 days

            messages.success(request, f"Welcome back {user.username}!")
            return redirect("home")  # Redirect to home page after login

        # Invalid credentials → show error message
        messages.error(request, "Invalid username or password")

    else:
        # GET request → blank form
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
            messages.success(
                request,
                f"Account created successfully for: '{user.username}'!"
            )
            return redirect("home")

        # Form is invalid — custom messages are already handled by the form
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


# account Settings & Delete

@login_required
def delete_account(request):
    """
    Delete the user account.

    Deletes the user account and all associated data:
    plants, tasks and beds.
    """

    # Prevent superusers from deleting themselves via the user-facing UI
    if request.user.is_superuser:
        messages.error(
            request,
            "Admin accounts cannot be deleted from this page."
        )
        return redirect("account_settings")

    if request.method == "POST":
        user = request.user
        logout(request)        # end session cleanly
        user.delete()          # cascades through all related models
        return redirect("login")

    return render(request, "accounts/delete_account.html")


@login_required
def account_settings(request):
    """
    Account settings view.

    Allows the user to delete their account or reset their password.
    """
    return render(request, "accounts/account_settings.html")


@login_required
def update_account(request):
    """
    Allow the logged-in user to update their account details.

    Currently supports:
    - Updating email address

    Future-ready for:
    - First name
    - Last name
    - Additional profile fields
    """
    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your account details have been updated."
            )
            return redirect("account_settings")
    else:
        form = AccountUpdateForm(instance=request.user)

    return render(request, "accounts/account_edit.html", {"form": form})
