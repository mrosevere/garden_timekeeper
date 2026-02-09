"""
The core app does not define database models by default.

This module exists to allow future expansion, such as shared abstract models,
timestamp mixins, or reusable base classes that can be inherited by models
in other apps.
"""

from django.db import models
from django.contrib.auth.models import User


class GardenBed(models.Model):
    """A physical garden bed or container owned by a user."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="garden_beds"
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
