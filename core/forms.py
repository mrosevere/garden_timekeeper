from django import forms
from .models import GardenBed, Plant, PlantTask
from crispy_forms.helper import FormHelper


# -----------------------------------------------------
#       Garden Bed Form
# -----------------------------------------------------
class GardenBedForm(forms.ModelForm):
    """
    A ModelForm for creating and editing GardenBed instances.

    This form provides Bootstrap styled widgets for all fields to
    ensure consistent UI across the application. It exposes the
    name, location, and description fields from the GardenBed model.
    """

    class Meta:
        """
        Form for creating/editing Garden Beds.

        The "description" field is presented as optional Notes to encourage
        users to record useful growing conditions or reminders.
        """
        model = GardenBed
        fields = ["name", "location", "description"]

        # Label the description field as "Notes" as better UX
        labels = {
            "description": "Notes",
        }

        # Add helper text to explain field usage.
        help_texts = {
            "description":
                "Example: Full sun, dries out quickly, slug-prone area.",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}),
            "location": forms.TextInput(
                attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": (
                        "optional additional notes"
                    ),
                    }
                ),
        }


# -----------------------------------------------------
#       Plant Form
# -----------------------------------------------------
class PlantForm(forms.ModelForm):
    """
    A ModelForm for creating and editing Plant instances.

    This form includes fields for botanical and lifecycle information,
    including name, Latin name, lifespan classification, plant type,
    planting date, and optional notes.

    Bootstrap-compatible widgets are applied to ensure a clean and
    consistent user experience. Layout is handled in the template
    (for consistency with the Task form).
    """

    class Meta:
        model = Plant
        fields = [
            "name",
            "latin_name",
            "image",
            "bed",
            "lifespan",
            "type",
            "planting_date",
            "notes",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "latin_name": forms.TextInput(attrs={"class": "form-control"}),
            "lifespan": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "planting_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "bed": forms.Select(attrs={"class": "form-select"}),

            # Replace SummernoteWidget with a plain textarea
            "notes": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Restrict beds to the current user
        if user is not None:
            self.fields["bed"].queryset = GardenBed.objects.filter(owner=user)
        else:
            self.fields["bed"].queryset = GardenBed.objects.none()

        # Crispy helper (same as Task)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.include_media = False


# -----------------------------------------------------
#       Task Form
# -----------------------------------------------------
class PlantTaskForm(forms.ModelForm):
    """
    A ModelForm for creating and editing Plant Tasks.

    This form includes fields for task information,
    including name, notes, dates task needs to be performed

    """
    class Meta:
        model = PlantTask
        # fix bug 109
        exclude = ["plant", "user", "last_done", "next_due"]
        labels = {
            "name": "Task Name",
        }
        fields = "__all__"
