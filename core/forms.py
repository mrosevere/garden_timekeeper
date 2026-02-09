from django import forms
from .models import GardenBed


class GardenBedForm(forms.ModelForm):
    class Meta:
        model = GardenBed
        fields = ["name", "location", "description"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control"
                }),
            "location": forms.TextInput(attrs={
                "class": "form-control"
                }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
                })
        }
