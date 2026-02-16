"""
Custom form classes for user authentication and registration.

This module provides:
- RegistrationForm: extends Django's UserCreationForm with an email field
  and consistent Bootstrap styling.
- LoginForm: extends Django's AuthenticationForm to apply Bootstrap styling
  and integrate cleanly with the login view.

These forms centralise widget configuration, validation behaviour, and
presentation logic, keeping the views clean and maintainable.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Custom registration form for the Garden Timekeeper application.

    Enhancements over Django's built-in UserCreationForm:
    - Adds a required email field
    - Applies Bootstrap-friendly CSS classes to all fields
    - Provides clearer error messages for username and password validation
    - Keeps form logic clean and centralised for maintainability
    """

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    # Override default password mismatch message
    error_messages = {
        "password_mismatch": "Passwords do not match",
    }

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"]

        # Custom error messages for specific fields
        error_messages = {
            "username": {
                "unique": "Username already taken",
                "required": "Please enter a username",
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Apply consistent Bootstrap styling to all fields.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class LoginForm(AuthenticationForm):
    """
    Custom login form used by the login view.

    Enhancements over Django's AuthenticationForm:
    - Applies Bootstrap styling to username and password fields
    - Keeps the login view clean and focused on flow control
    """

    def __init__(self, *args, **kwargs):
        """
        Apply Bootstrap styling to login fields.
        """
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
        })


class AccountUpdateForm(forms.ModelForm):
    """
    Form used to update the logged-in user's account details.

    Currently supports:
    - Username (cannot be edited)
    - First name
    - Last name
    - Email address

    Future-ready for additional profile fields.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
            })

        # Optional placeholders for nicer UX
        self.fields["first_name"].widget.attrs.update({
            "placeholder": "First name",
        })
        self.fields["last_name"].widget.attrs.update({
            "placeholder": "Last name",
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "Email address",
        })

    def clean_email(self):
        email = self.cleaned_data["email"]

        # Prevent duplicate emails (excluding the current user)
        if (
            User.objects.filter(email=email)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "This email address is already in use."
            )

        return email
