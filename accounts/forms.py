from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """
    Custom registration form for the Garden Timekeeper application.

    Extends Django's built-in UserCreationForm by:
    - Adding an email field
    - Applying Bootstrap-friendly CSS classes to all fields
    - Overriding default error messages for clearer user feedback
    - Providing a clean, structure for validation
    """
    # Django's UserCreationForm contains:
    # self.fields["username"]
    # self.fields["password1"]
    # self.fields["password2"]
    # Now extend it with:
    email = forms.EmailField(required=True)

    # This needs to be done first as error handling done before view
    error_messages = {
                      "password_mismatch": "Passwords do not match",
                      }

    class Meta:
        model = User
        # Define the form fields
        fields = ["username", "email", "password1", "password2"]

        # Custom error messages that match your test suite
        error_messages = {
            "username": {
                "unique": "Username already taken",
                "required": "Please enter a username",
            },
        }

    def __init__(self, *args, **kwargs):
        """
        Initialise the form and apply Bootstrap CSS classes to all fields.

        This ensures consistent styling across the registration page without
        requiring manual class assignment in the template.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
