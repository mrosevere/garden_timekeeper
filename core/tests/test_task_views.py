from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core.models import Plant, GardenBed, PlantTask, PlantType, PlantLifespan
from core.forms import PlantTaskForm
import datetime

User = get_user_model()


# =========================================================
# TASK MODEL TESTS
# =========================================================

class PlantTaskModelValidationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.bed = GardenBed.objects.create(owner=self.user, name="Main Bed")
        self.plant = Plant.objects.create(
            owner=self.user,
            name="Tomato",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.PERENNIAL,
            bed=self.bed,
        )

    def test_name_required(self):
        with self.assertRaises(IntegrityError):
            PlantTask.objects.create(
                user=self.user,
                plant=self.plant,
                name="",
                frequency="7d",
            )

    def test_frequency_required(self):
        with self.assertRaises(IntegrityError):
            PlantTask.objects.create(
                user=self.user,
                plant=self.plant,
                name="Watering",
                frequency="",
            )


# =========================================================
# TASK FORM TESTS
# =========================================================

class PlantTaskFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.bed = GardenBed.objects.create(owner=self.user, name="Main Bed")
        self.plant = Plant.objects.create(
            owner=self.user,
            name="Tomato",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.PERENNIAL,
            bed=self.bed,
        )

    def test_valid_form(self):
        form = PlantTaskForm(data={
            "name": "Watering",
            "frequency": "7d",
            "all_year": True,
            "seasonal_start_month": 1,
            "seasonal_end_month": 12,
            "repeat": True,
        })
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        form = PlantTaskForm(data={
            "name": "",
            "frequency": "7d",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_frequency_required(self):
        form = PlantTaskForm(data={
            "name": "Watering",
            "frequency": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("frequency", form.errors)

    def test_invalid_frequency_format(self):
        form = PlantTaskForm(data={
            "name": "Watering",
            "frequency": "invalid",
        })
        self.assertFalse(form.is_valid())


# =========================================================
# TASK VIEW TESTS
# =========================================================

class TaskViewTests(TestCase):

    def setUp(self):
        # Users
        self.user = User.objects.create_user(username="mark", password="pass")
        self.other_user = User.objects.create_user(
            username="other", password="pass"
        )

        # Beds
        self.bed = GardenBed.objects.create(owner=self.user, name="Main Bed")
        self.other_bed = GardenBed.objects.create(
            owner=self.other_user, name="Other Bed"
        )

        # Plants
        self.plant = Plant.objects.create(
            owner=self.user,
            name="Tomato",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.PERENNIAL,
            bed=self.bed,
        )

        self.other_plant = Plant.objects.create(
            owner=self.other_user,
            name="Carrot",
            type=PlantType.VEGETABLE,
            lifespan=PlantLifespan.PERENNIAL,
            bed=self.other_bed,
        )

        # Tasks
        self.task = PlantTask.objects.create(
            user=self.user,
            plant=self.plant,
            name="Watering",
            frequency="7d",
            last_done=datetime.date(2024, 1, 1),
            next_due=datetime.date(2024, 1, 8),
        )

        self.other_task = PlantTask.objects.create(
            user=self.other_user,
            plant=self.other_plant,
            name="Pruning",
            frequency="7d",
            last_done=datetime.date(2024, 1, 1),
            next_due=datetime.date(2024, 1, 8),
        )

    # ---------------------------------------------------------
    # LOGIN REQUIRED
    # ---------------------------------------------------------

    def test_task_detail_requires_login(self):
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_task_edit_requires_login(self):
        response = self.client.get(reverse("task_update", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_task_delete_requires_login(self):
        response = self.client.get(reverse("task_delete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_task_mark_done_requires_login(self):
        response = self.client.get(
            reverse("task_mark_done", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_task_skip_requires_login(self):
        response = self.client.get(reverse("task_skip", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    # ---------------------------------------------------------
    # DETAIL VIEW
    # ---------------------------------------------------------

    def test_user_can_view_own_task_detail(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("task_detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_view_other_users_task(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("task_detail", args=[self.other_task.pk])
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # CREATE VIEW
    # ---------------------------------------------------------

    def test_user_can_create_task_for_own_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("task_create", args=[self.plant.pk]),
            {
                "name": "Feeding",
                "frequency": "7d",
                "all_year": True,
                "seasonal_start_month": 1,
                "seasonal_end_month": 12,
                "repeat": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        task = PlantTask.objects.get(name="Feeding")
        self.assertIsNotNone(task.next_due)

    def test_user_cannot_create_task_for_other_users_plant(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("task_create", args=[self.other_plant.pk]),
            {"name": "Hacked Task", "frequency": "7d"},
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # EDIT VIEW
    # ---------------------------------------------------------

    def test_user_can_edit_own_task(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("task_update", args=[self.task.pk]),
            {
                "name": "Updated Watering",
                "frequency": "14d",
                "all_year": True,
                "seasonal_start_month": 1,
                "seasonal_end_month": 12,
                "repeat": True,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Watering")

    def test_user_cannot_edit_other_users_task(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("task_update", args=[self.other_task.pk]),
            {"name": "Hacked", "frequency": "14d"},
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # DELETE VIEW
    # ---------------------------------------------------------

    def test_user_can_delete_own_task(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("task_delete", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PlantTask.objects.filter(pk=self.task.pk).exists())

    def test_user_cannot_delete_other_users_task(self):
        self.client.login(username="mark", password="pass")
        response = self.client.post(
            reverse("task_delete", args=[self.other_task.pk])
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # MARK DONE
    # ---------------------------------------------------------

    def test_user_can_mark_task_done(self):
        self.client.login(username="mark", password="pass")
        old_due = self.task.next_due
        response = self.client.get(
            reverse("task_mark_done", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()
        self.assertNotEqual(self.task.next_due, old_due)
        self.assertIsNotNone(self.task.last_done)

    def test_user_cannot_mark_other_users_task_done(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("task_mark_done", args=[self.other_task.pk])
        )
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------
    # SKIP
    # ---------------------------------------------------------

    def test_user_can_skip_own_task(self):
        self.client.login(username="mark", password="pass")
        old_due = self.task.next_due
        response = self.client.get(reverse("task_skip", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()
        self.assertGreater(self.task.next_due, old_due)

    def test_user_cannot_skip_other_users_task(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(
            reverse("task_skip", args=[self.other_task.pk])
        )
        self.assertEqual(response.status_code, 404)
