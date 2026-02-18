"""
tests for the beds pages.

Covers:
- xx

To skip a test, use: #@skip("<enter your skip message here>")
"""

from django.test import TestCase
from unittest import skip
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import GardenBed


class BedsTests(TestCase):
    """Test suite for beds-related views."""

    def test_bed_list_requires_login(self):
        response = self.client.get(reverse("bed_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_bed_list_shows_only_user_beds(self):
        # Beds for two different users
        user1 = self.user
        user2 = User.objects.create_user(username="other", password="pass1234")

        GardenBed.objects.create(owner=user1, name="Mark's Bed")
        GardenBed.objects.create(owner=user2, name="Other User Bed")

        self.client.login(username="mark", password="testpass123")
        response = self.client.get(reverse("bed_list"))

        self.assertContains(response, "Mark's Bed")
        self.assertNotContains(response, "Other User Bed")

    def test_bed_detail_requires_login(self):
        bed = GardenBed.objects.create(owner=self.user, name="Test Bed")

        response = self.client.get(reverse("bed_detail", args=[bed.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_bed_detail_loads_for_owner(self):
        bed = GardenBed.objects.create(owner=self.user, name="Test Bed")

        self.client.login(username="mark", password="testpass123")
        response = self.client.get(reverse("bed_detail", args=[bed.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/beds/bed_detail.html")
        self.assertContains(response, "Test Bed")

    def test_bed_detail_cannot_be_accessed_by_other_user(self):
        owner = self.user
        other_user = User.objects.create_user(
            username="other", password="pass1234"
            )

        bed = GardenBed.objects.create(owner=owner, name="Private Bed")

        self.client.login(username="other", password="pass1234")

        response = self.client.get(reverse("bed_detail", args=[bed.pk]))

        # Should return 404, not 403 — this hides the existence of the bed
        self.assertEqual(response.status_code, 404)

    def test_beds_are_ordered_by_name(self):
        self.client.login(username="mark", password="testpass123")

        GardenBed.objects.create(owner=self.user, name="Z Bed")
        GardenBed.objects.create(owner=self.user, name="A Bed")

        response = self.client.get(reverse("bed_list"))
        content = response.content.decode()

        self.assertTrue(content.index("A Bed") < content.index("Z Bed"))
