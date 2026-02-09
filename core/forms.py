from django import forms
from .models import GardenBed, Plant


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
        }
