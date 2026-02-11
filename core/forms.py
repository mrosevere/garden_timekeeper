from django import forms
from .models import GardenBed, Plant, PlantTask
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML


class GardenBedForm(forms.ModelForm):
    """
    A ModelForm for creating and editing GardenBed instances.

    This form provides Bootstrap styled widgets for all fields to
    ensure consistent UI across the application. It exposes the
    name, location, and description fields from the GardenBed model.
    """

    class Meta:
        model = GardenBed
        fields = ["name", "location", "description"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}),
            "location": forms.TextInput(
                attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}),
        }


class PlantForm(forms.ModelForm):
    """
    A ModelForm for creating and editing Plant instances.

    This form includes fields for botanical and lifecycle information,
    including name, Latin name, lifespan classification, plant type,
    planting date, and optional notes.
    Bootstrap compatible widgets are applied to ensure a clean and
    consistent user experience.
    """

    class Meta:
        model = Plant
        fields = [
            "name",
            "latin_name",
            "bed",
            "lifespan",
            "type",
            "planting_date",
            "notes"
            ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}),
            "latin_name": forms.TextInput(
                attrs={"class": "form-control"}),
            "lifespan": forms.Select(
                attrs={"class": "form-select"}),
            "type": forms.Select(
                attrs={"class": "form-select"}),
            "planting_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}),
            "bed": forms.Select(
                attrs={"class": "form-select"}),
            "notes": forms.Textarea(
                attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        """
        Initialise the PlantForm with user specific context.

        This override extracts the logged in user from the form kwargs and
        restricts the 'bed' field queryset to only the GardenBed instances
        owned by that user. This ensures users can assign plants only to
        their own beds and prevents cross user data exposure.
        kwargs = keyword arguments
        *args = collects positional arguments into a tuple
        **kwargs = collects keyword arguments into a dictionary
        """
        # remove user from kwargs dictionary,
        # because ModelForm.__init__ does not expect a user
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Crispy layout override
        self.helper = FormHelper()
        # prevents crispy from wrapping the form
        self.helper.form_tag = False
        # crispy won’t inject hidden fields
        self.helper.disable_csrf = True
        # prevents crispy from injecting extra fields
        self.helper.include_media = False
        # prevents auto rendering of beds
        self.helper.render_unmentioned_fields = False

        # Define the layout to set position of custom bed field.
        self.helper.layout = Layout(
            "name",
            "latin_name",

            HTML("""
                <div class="mb-3">
                    {{ form.bed.label_tag }}
                    <div class="d-flex align-items-center gap-2">
                    {{ form.bed }}
                    <a
                        href="{% url 'bed_create' %}"
                        data-bs-toggle="modal"
                        data-bs-target="#createBedModal"
                        class="btn btn-outline-secondary btn-sm"
                    >
                        + Add new bed
                    </a>
                    </div>
                </div>
            """),

            "lifespan",
            "type",
            "planting_date",
            "notes",
        )

        # Apply queryset filtering
        self.fields["bed"].queryset = GardenBed.objects.filter(owner=user)


class PlantTaskForm(forms.ModelForm):
    """
    A ModelForm for creating and editing Plant Tasks.

    This form includes fields for task information,
    including name, notes, dates task needs to be performed

    """
    class Meta:
        model = PlantTask
        fields = [
            "name",
            "all_year",
            "seasonal_start_month",
            "seasonal_end_month",
            "frequency",
            "repeat",
            "notes",
        ]
