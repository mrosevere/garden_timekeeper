"""
The core app models
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.conf import settings


# ================= Garden Bed Models =================
class GardenBed(models.Model):
    """A physical garden bed or container owned by a user."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="garden_beds"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "owner",
                name="unique_bed_name_per_user_case_insensitive"
            )
        ]

    def __str__(self):
        return self.name


# ================= PLANT MODELS =================
class PlantType(models.TextChoices):
    # Constant = DBValue, Label
    VEGETABLE = "VEG", "Vegetable"
    FRUIT = "FRU", "Fruit"
    HERB = "HER", "Herb"
    FLOWER = "FLO", "Flower"
    SHRUB = "SHR", "Shrub"
    TREE = "TRE", "Tree"


class PlantLifespan(models.TextChoices):
    # Constant = DBValue, Label
    ANNUAL = "ANN", "Annual"
    PERENNIAL = "PER", "Perennial"
    BIENNIAL = "BIE", "Biennial"


class Plant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plants"
    )
    name = models.CharField(max_length=100)
    latin_name = models.CharField(max_length=100, blank=True)
    lifespan = models.CharField(
        choices=PlantLifespan.choices,
        default=PlantLifespan.PERENNIAL,
    )
    type = models.CharField(
        choices=PlantType.choices,
    )
    planting_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
