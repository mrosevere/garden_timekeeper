from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Plant, GardenBed, PlantType, PlantLifespan


class PlantViewTests(TestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(
            username="mark", password="pass"
        )
        self.other_user = User.objects.create_user(
            username="other", password="pass"
        )

        # Beds
        self.bed1 = GardenBed.objects.create(
            owner=self.user, name="Bed A"
        )
        self.bed2 = GardenBed.objects.create(
            owner=self.user, name="Bed B"
        )
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
        self.assertIn("/accounts/login/", response.url)

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

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/plants/plant_list.html")

        # Your view must expose "plants" in context
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

        response = self.client.get(
            reverse("plant_list") + f"?bed={self.bed1.id}"
        )
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

        response = self.client.get(
            reverse("plant_list") + "?sort=name&direction=desc"
        )
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
        self.assertTemplateUsed(response, "core/plants/plant_detail.html")

    def test_user_cannot_view_other_users_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("plant_detail", args=[self.other_plant.pk])
        )

        self.assertEqual(response.status_code, 404)
