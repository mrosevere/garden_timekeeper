from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from core.models import Plant, GardenBed, PlantType, PlantLifespan
from core.forms import PlantForm

User = get_user_model()


# =========================================================
# PLANT MODEL TESTS
# =========================================================

class PlantModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.bed = GardenBed.objects.create(owner=self.user, name="Bed A")

    def test_string_representation(self):
        plant = Plant.objects.create(
            owner=self.user,
            name="Tomato",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.ANNUAL,
            bed=self.bed,
        )
        self.assertEqual(str(plant), "Tomato")

    def test_name_required(self):
        with self.assertRaises(IntegrityError):
            Plant.objects.create(
                owner=self.user,
                name="",
                type=PlantType.VEGETABLE,
                lifespan=PlantLifespan.ANNUAL,
                bed=self.bed,
            )

    def test_bed_optional(self):
        plant = Plant.objects.create(
            owner=self.user,
            name="Rose",
            type=PlantType.FLOWER,
            lifespan=PlantLifespan.PERENNIAL,
            bed=None,
        )
        self.assertIsNone(plant.bed)


# =========================================================
# PLANT FORM TESTS
# =========================================================

class PlantFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.bed = GardenBed.objects.create(owner=self.user, name="Bed A")

    def test_valid_form(self):
        form = PlantForm(
            data={
                "name": "Tomato",
                "type": PlantType.VEGETABLE,
                "lifespan": PlantLifespan.ANNUAL,
                "bed": self.bed.id,
            },
            user=self.user,  # <-- required
        )
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        form = PlantForm(data={
            "name": "",
            "type": PlantType.VEGETABLE,
            "lifespan": PlantLifespan.ANNUAL,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_invalid_type(self):
        form = PlantForm(data={
            "name": "Test",
            "type": "INVALID",
            "lifespan": PlantLifespan.ANNUAL,
        })
        self.assertFalse(form.is_valid())


# =========================================================
# PLANT VIEW TESTS (YOUR EXISTING TESTS + NEW ONES)
# =========================================================

class PlantViewTests(TestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="mark", password="pass")
        self.other_user = User.objects.create_user(
            username="other", password="pass"
        )

        # Beds
        self.bed1 = GardenBed.objects.create(owner=self.user, name="Bed A")
        self.bed2 = GardenBed.objects.create(owner=self.user, name="Bed B")
        self.other_bed = GardenBed.objects.create(
            owner=self.other_user, name="Other Bed"
        )

        # Plants
        self.plant1 = Plant.objects.create(
            owner=self.user,
            name="Tomato",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.ANNUAL,
            bed=self.bed1,
        )

        self.plant2 = Plant.objects.create(
            owner=self.user,
            name="Rose",
            type=PlantType.FLOWER,
            lifespan=PlantLifespan.PERENNIAL,
            bed=self.bed2,
        )

        self.other_plant = Plant.objects.create(
            owner=self.other_user,
            name="Carrot",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.ANNUAL,
            bed=self.other_bed,
        )

    # ---------------------------------------------------------
    # LOGIN REQUIRED
    # ---------------------------------------------------------

    def test_plant_list_requires_login(self):
        response = self.client.get(reverse("plant_list"))
        self.assertEqual(response.status_code, 302)

    def test_plant_detail_requires_login(self):
        response = self.client.get(
            reverse("plant_detail", args=[self.plant1.pk])
        )
        self.assertEqual(response.status_code, 302)

    # ---------------------------------------------------------
    # LIST VIEW
    # ---------------------------------------------------------

    def test_user_sees_only_their_own_plants(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("plant_list"))

        plants = response.context["plants"]
        self.assertIn(self.plant1, plants)
        self.assertIn(self.plant2, plants)
        self.assertNotIn(self.other_plant, plants)

    def test_plant_list_search_filter(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("plant_list") + "?search=tom")
        plants = response.context["plants"]
        self.assertIn(self.plant1, plants)
        self.assertNotIn(self.plant2, plants)

    def test_plant_list_filter_by_bed(self):
        self.client.login(username="mark", password="pass")
        url = reverse("plant_list") + f"?bed={self.bed1.id}"
        response = self.client.get(url)
        plants = response.context["plants"]
        self.assertIn(self.plant1, plants)
        self.assertNotIn(self.plant2, plants)

    def test_plant_list_filter_by_type(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("plant_list") + "?type=FLO")
        plants = response.context["plants"]
        self.assertIn(self.plant2, plants)
        self.assertNotIn(self.plant1, plants)

    def test_plant_list_filter_by_lifespan(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("plant_list") + "?lifespan=ANN")
        plants = response.context["plants"]
        self.assertIn(self.plant1, plants)
        self.assertNotIn(self.plant2, plants)

    def test_plant_list_sorting(self):
        self.client.login(username="mark", password="pass")
        url = reverse("plant_list") + "?sort=name&direction=desc"
        response = self.client.get(url)
        plants = list(response.context["plants"])
        self.assertEqual(plants[0], self.plant1)  # Tomato
        self.assertEqual(plants[1], self.plant2)  # Rose

    # ---------------------------------------------------------
    # DETAIL VIEW
    # ---------------------------------------------------------

    def test_user_can_view_own_plant_detail(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("plant_detail", args=[self.plant1.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_view_other_users_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("plant_detail", args=[self.other_plant.pk])
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # CREATE VIEW
    # ---------------------------------------------------------

    def test_create_requires_login(self):
        response = self.client.get(reverse("plant_create"))
        self.assertEqual(response.status_code, 302)

    def test_user_can_create_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(reverse("plant_create"), {
            "name": "New Plant",
            "type": PlantType.VEGETABLE,
            "lifespan": PlantLifespan.ANNUAL,
            "bed": self.bed1.id,
        })
        self.assertEqual(Plant.objects.filter(owner=self.user).count(), 3)
        self.assertRedirects(response, reverse("plant_list"))

    # ---------------------------------------------------------
    # UPDATE VIEW
    # ---------------------------------------------------------

    def test_edit_requires_login(self):
        response = self.client.get(
            reverse("plant_edit", args=[self.plant1.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_user_can_edit_own_plant(self):
        self.client.login(username="mark", password="pass")

        self.client.post(
            reverse("plant_edit", args=[self.plant1.id]),
            {
                "name": "Updated Tomato",
                "type": PlantType.VEGETABLE,
                "lifespan": PlantLifespan.ANNUAL,
                "bed": self.bed2.id,
            }
        )

        self.plant1.refresh_from_db()
        self.assertEqual(self.plant1.name, "Updated Tomato")
        self.assertEqual(self.plant1.bed, self.bed2)

    def test_user_cannot_edit_other_users_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("plant_edit", args=[self.other_plant.id])
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # DELETE VIEW
    # ---------------------------------------------------------

    def test_delete_requires_login(self):
        response = self.client.get(
            reverse("plant_delete", args=[self.plant1.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_user_can_delete_own_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("plant_delete", args=[self.plant1.id])
        )
        self.assertFalse(Plant.objects.filter(id=self.plant1.id).exists())
        self.assertRedirects(response, reverse("plant_list"))

    def test_user_cannot_delete_other_users_plant(self):
        self.client.login(username="mark", password="pass")
        self.client.post(
            reverse("plant_delete", args=[self.other_plant.id])
        )
        self.assertTrue(Plant.objects.filter(id=self.other_plant.id).exists())
