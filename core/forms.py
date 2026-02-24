from django import forms
from django.forms.widgets import ClearableFileInput
from .models import GardenBed, Plant, PlantTask
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


# ====================================================
#       Garden Bed Form
# ====================================================
class GardenBedForm(forms.ModelForm):
    """
    A ModelForm for creating and editing GardenBed instances.
    Includes duplicate-name validation to prevent DB IntegrityErrors.
    """

    def __init__(self, *args, **kwargs):
        # Capture the user passed in from the view
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = GardenBed
        fields = ["name", "location", "description"]

        labels = {
            "description": "Notes",
        }

        help_texts = {
            "description":
                "Example: Full sun, dries out quickly, slug-prone area.",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "optional additional notes",
                }
            ),
        }

    # ====================================================
    #   Duplicate Name Validation (case-insensitive)
    # ====================================================
    def clean_name(self):
        """
        Prevent duplicate bed names (case-insensitive) for the same user.
        This avoids DB-level IntegrityErrors during tests.
        """
        name = self.cleaned_data["name"].strip()

        # Determine owner:
        # - CreateView: user passed via get_form_kwargs()
        # - UpdateView: instance.owner already set
        owner = self.user or getattr(self.instance, "owner", None)

        qs = GardenBed.objects.filter(owner=owner, name__iexact=name)

        # Exclude current instance when editing
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "You already have a bed with this name."
            )

        return name


# ====================================================
#       Plant Form
# ====================================================
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
            "name": forms.TextInput(
                attrs={"class": "form-control", "required": "required"}
            ),
            "latin_name": forms.TextInput(attrs={"class": "form-control"}),
            "lifespan": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "planting_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "bed": forms.Select(attrs={"class": "form-select"}),

            # set to clearable so user can delete an image
            "image": ClearableFileInput(attrs={"class": "form-control"}),

            # Notes changed to plain textarea (Summernote initialised manually)
            "notes": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # ====================================================
        # Fix summernote Aria issues
        # ====================================================
        self.fields['notes'].widget.attrs.update({
            'aria-label': 'Notes about this plant'
            })

        # ====================================================
        # Limit the "bed" dropdown to beds owned by the current user
        # ====================================================
        if user is not None:
            self.fields["bed"].queryset = GardenBed.objects.filter(
                owner=user
                )
        else:
            self.fields["bed"].queryset = GardenBed.objects.none()

        # ====================================================
        # Crispy helper setup
        # ====================================================
        self.helper = FormHelper()
        # Use custom setup rather than crispy default
        self.helper.form_tag = False
        self.helper.include_media = False

        # ====================================================
        # IMPORTANT:
        # Prevent crispy from rendering the "image" field automatically.
        #
        # Without this, crispy injects Django's default ClearableFileInput
        # block, which includes:
        #   - "Currently:"
        #   - the hashed filename
        #   - the default Clear checkbox
        #   - the "Change:" label
        #   - a duplicate file input
        #
        # Prevent crispy from generating a layout or auto‑rendering fields
        # We render a fully custom image section in the template, so we
        # explicitly exclude the field here.
        # ====================================================

        self.helper.layout = Layout()
        self.helper.exclude = ["image"]


# ====================================================
#       Task Form
# ====================================================
class PlantTaskForm(forms.ModelForm):
    """
    Form for creating and editing PlantTask objects.

    Enhancements:
    - Removes Django's autogenerated help text to prevent invalid
      aria-describedby attributes in custom templates.
    - Applies Bootstrap styling consistently.
    - Accepts a 'user' kwarg so the view can filter plant choices.
    """

    class Meta:
        model = PlantTask
        fields = [
            "name",
            "notes",
            "all_year",
            "seasonal_start_month",
            "seasonal_end_month",
            "frequency",
            "repeat",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Remove autogenerated help text (fixes HTML validator errors)
        for field in self.fields.values():
            field.help_text = None

        # Apply Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        # Boolean fields need form-check styling
        if "all_year" in self.fields:
            self.fields["all_year"].widget.attrs.update(
                {"class": "form-check-input"}
            )
