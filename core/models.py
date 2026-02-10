"""
The core app models
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.conf import settings


# ================= Garden Bed Models =================
class GardenBed(models.Model):
    """
    A physical garden bed or container owned by a user.

    A GardenBed stores basic descriptive information such as its name,
    location within the garden, and an optional description. Each bed is
    associated with a specific user, enabling personalised garden layouts.
    """

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
    """
    Plant type categories.

    These values classify the plant type. The stored values are short codes,
    while the human readable labels are used in forms and the admin interface.
    """
    # Constant = DBValue, Label
    VEGETABLE = "VEG", "Vegetable"
    FRUIT = "FRU", "Fruit"
    HERB = "HER", "Herb"
    FLOWER = "FLO", "Flower"
    SHRUB = "SHR", "Shrub"
    TREE = "TRE", "Tree"


class PlantLifespan(models.TextChoices):
    """
    Plant lifespan categories.

    These values classify how long a plant lives and therefore
    how it behaves in the garden. The stored values are short codes,
    while the human readable labels are used in forms and the admin interface.
    """

    # Constant = DBValue, Label
    ANNUAL = "ANN", "Annual"
    PERENNIAL = "PER", "Perennial"
    BIENNIAL = "BIE", "Biennial"


class Plant(models.Model):

    """
    Represents a plant grown by a user.

    A Plant stores botanical information such as its common name,
    optional Latin name, and lifespan classification.
    It also includes optional planting metadata and free text notes.
    Each plant is owned by a specific user,
    allowing personalised garden tracking.
    """

    owner = models.ForeignKey(
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
    bed = models.ForeignKey(
        GardenBed,
        on_delete=models.CASCADE,
        related_name="plants"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
