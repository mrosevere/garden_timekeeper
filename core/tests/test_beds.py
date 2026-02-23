from django.test import TestCase
from django.contrib.auth.models import User
from core.models import GardenBed


class BedsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.other_user = User.objects.create_user(username="other_user", password="pass")

    def test_bed_list_shows_only_user_beds(self):
        bed1 = GardenBed.objects.create(owner=self.user, name="A Bed")
        bed2 = GardenBed.objects.create(owner=self.other_user, name="Z Bed")

        self.client.login(username="mark", password="pass")
        response = self.client.get("/beds/")

        beds = response.context["object_list"]
        self.assertIn(bed1, beds)
        self.assertNotIn(bed2, beds)

    def test_bed_detail_cannot_be_accessed_by_other_user(self):
        bed = GardenBed.objects.create(owner=self.other_user, name="Other Bed")

        self.client.login(username="mark", password="pass")
        response = self.client.get(f"/beds/{bed.pk}/")

        self.assertEqual(response.status_code, 404)

    def test_beds_are_ordered_by_name(self):
        GardenBed.objects.create(owner=self.user, name="Z Bed")
        GardenBed.objects.create(owner=self.user, name="A Bed")

        self.client.login(username="mark", password="pass")
        response = self.client.get("/beds/")

        beds = list(response.context["object_list"])
        self.assertEqual([b.name for b in beds], ["A Bed", "Main Bed", "Z Bed"])
