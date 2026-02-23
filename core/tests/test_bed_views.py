from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import GardenBed


class BedViewTests(TestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="mark", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")

        # Beds
        self.bed1 = GardenBed.objects.create(owner=self.user, name="A Bed", location="North")
        self.bed2 = GardenBed.objects.create(owner=self.user, name="Z Bed", location="South")
        self.other_bed = GardenBed.objects.create(owner=self.other_user, name="Other Bed")

    # ---------------------------------------------------------
    # LOGIN REQUIRED
    # ---------------------------------------------------------

    def test_bed_list_requires_login(self):
        response = self.client.get(reverse("bed_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_bed_detail_requires_login(self):
        response = self.client.get(reverse("bed_detail", args=[self.bed1.pk]))
        self.assertEqual(response.status_code, 302)

    def test_bed_create_requires_login(self):
        response = self.client.get(reverse("bed_create"))
        self.assertEqual(response.status_code, 302)

    def test_bed_edit_requires_login(self):
        response = self.client.get(reverse("bed_edit", args=[self.bed1.pk]))
        self.assertEqual(response.status_code, 302)

    def test_bed_delete_requires_login(self):
        response = self.client.get(reverse("bed_delete", args=[self.bed1.pk]))
        self.assertEqual(response.status_code, 302)

    # ---------------------------------------------------------
    # LIST VIEW
    # ---------------------------------------------------------

    def test_bed_list_shows_only_user_beds(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("bed_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/beds/bed_list.html")

        # Your view must expose "beds" in context
        beds = response.context["beds"]

        self.assertIn(self.bed1, beds)
        self.assertIn(self.bed2, beds)
        self.assertNotIn(self.other_bed, beds)

    def test_bed_list_search_filter(self):
        self.client.login(username="mark", password="pass")

        response = self.client.get(reverse("bed_list") + "?search=A")
        beds = response.context["beds"]

        self.assertIn(self.bed1, beds)
        self.assertNotIn(self.bed2, beds)

    def test_bed_list_location_filter(self):
        self.client.login(username="mark", password="pass")

        response = self.client.get(reverse("bed_list") + "?location=North")
        beds = response.context["beds"]

        self.assertIn(self.bed1, beds)
        self.assertNotIn(self.bed2, beds)

    def test_bed_list_sorting(self):
        self.client.login(username="mark", password="pass")

        response = self.client.get(reverse("bed_list") + "?sort=name&direction=desc")
        beds = list(response.context["beds"])

        self.assertEqual(beds[0], self.bed2)  # Z Bed
        self.assertEqual(beds[1], self.bed1)  # A Bed

    # ---------------------------------------------------------
    # DETAIL VIEW
    # ---------------------------------------------------------

    def test_user_can_view_own_bed_detail(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("bed_detail", args=[self.bed1.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/beds/bed_detail.html")

    def test_user_cannot_view_other_users_bed(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("bed_detail", args=[self.other_bed.pk]))

        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # CREATE VIEW
    # ---------------------------------------------------------

    def test_user_can_create_bed(self):
        self.client.login(username="mark", password="pass")

        response = self.client.post(reverse("bed_create"), {
            "name": "Herb Bed",
            "description": "A small herb bed",
            "location": "Corner",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(GardenBed.objects.filter(name="Herb Bed", owner=self.user).exists())

    # ---------------------------------------------------------
    # EDIT VIEW
    # ---------------------------------------------------------

    def test_user_can_edit_own_bed(self):
        self.client.login(username="mark", password="pass")

        response = self.client.post(reverse("bed_edit", args=[self.bed1.pk]), {
            "name": "Updated Bed",
            "description": "Updated description",
            "location": "Updated location",
        })

        self.assertEqual(response.status_code, 302)
        self.bed1.refresh_from_db()
        self.assertEqual(self.bed1.name, "Updated Bed")

    def test_user_cannot_edit_other_users_bed(self):
        self.client.login(username="mark", password="pass")

        response = self.client.post(reverse("bed_edit", args=[self.other_bed.pk]), {
            "name": "Hacked",
            "description": "Hacked",
            "location": "Hacked",
        })

        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # DELETE VIEW
    # ---------------------------------------------------------

    def test_user_can_delete_own_bed(self):
        self.client.login(username="mark", password="pass")

        response = self.client.post(reverse("bed_delete", args=[self.bed1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(GardenBed.objects.filter(pk=self.bed1.pk).exists())

    def test_user_cannot_delete_other_users_bed(self):
        self.client.login(username="mark", password="pass")

        response = self.client.post(reverse("bed_delete", args=[self.other_bed.pk]))
        self.assertEqual(response.status_code, 404)
