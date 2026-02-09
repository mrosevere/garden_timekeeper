"""
The core app does not define database models by default.

This module exists to allow future expansion, such as shared abstract models,
timestamp mixins, or reusable base classes that can be inherited by models
in other apps.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower


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
