import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import IntegrityError

from core.models import (
    Plant,
    GardenBed,
    PlantTask,
    PlantType,
    PlantLifespan,
)


# =========================================================
# PLANT TASK MODEL TESTS (UNCHANGED)
# =========================================================

class PlantTaskModelTests(TestCase):

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

    # ---------------------------------------------------------
    # FREQUENCY PARSING
    # ---------------------------------------------------------

    def test_get_frequency_delta_days(self):
        task = PlantTask(frequency="7d")
        delta = task.get_frequency_delta()
        self.assertEqual(delta, {"days": 7, "months": 0})

    def test_get_frequency_delta_months(self):
        task = PlantTask(frequency="3m")
        delta = task.get_frequency_delta()
        self.assertEqual(delta, {"days": 0, "months": 3})

    # ---------------------------------------------------------
    # ADD MONTHS
    # ---------------------------------------------------------

    def test_add_months_handles_month_rollover(self):
        task = PlantTask()
        date_in = datetime.date(2024, 1, 31)
        result = task.add_months(date_in, 1)
        self.assertEqual(result, datetime.date(2024, 2, 29))  # leap year

    # ---------------------------------------------------------
    # SEASONAL LOGIC
    # ---------------------------------------------------------

    def test_is_in_season_all_year(self):
        task = PlantTask(all_year=True)
        self.assertTrue(task.is_in_season(datetime.date(2024, 5, 1)))

    def test_is_in_season_within_window(self):
        task = PlantTask(
            all_year=False,
            seasonal_start_month=4,
            seasonal_end_month=6,
        )
        self.assertTrue(task.is_in_season(datetime.date(2024, 5, 1)))

    def test_is_in_season_outside_window(self):
        task = PlantTask(
            all_year=False,
            seasonal_start_month=4,
            seasonal_end_month=6,
        )
        self.assertFalse(task.is_in_season(datetime.date(2024, 2, 1)))

    def test_is_in_season_wraparound(self):
        task = PlantTask(
            all_year=False,
            seasonal_start_month=11,
            seasonal_end_month=2,
        )
        self.assertTrue(task.is_in_season(datetime.date(2024, 12, 1)))
        self.assertTrue(task.is_in_season(datetime.date(2024, 1, 1)))
        self.assertFalse(task.is_in_season(datetime.date(2024, 6, 1)))

    # ---------------------------------------------------------
    # NEXT DUE — NEW TASKS
    # ---------------------------------------------------------

    def test_next_due_for_new_task_in_season(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            all_year=False,
            seasonal_start_month=5,
            seasonal_end_month=9,
        )

        test_date = datetime.date(2024, 5, 1)
        result = task.calculate_next_due(from_date=test_date)
        self.assertEqual(result, test_date)

    def test_next_due_for_new_task_before_season(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            all_year=False,
            seasonal_start_month=6,
            seasonal_end_month=9,
        )

        test_date = datetime.date(2024, 3, 1)
        result = task.calculate_next_due(from_date=test_date)
        self.assertEqual(result, datetime.date(2024, 6, 1))

    def test_next_due_for_new_task_after_season(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            all_year=False,
            seasonal_start_month=4,
            seasonal_end_month=6,
        )

        test_date = datetime.date(2024, 12, 1)
        result = task.calculate_next_due(from_date=test_date)
        self.assertEqual(result, datetime.date(2025, 4, 1))

    # ---------------------------------------------------------
    # NEXT DUE — RECURRING TASKS
    # ---------------------------------------------------------

    def test_next_due_recurring_daily(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            frequency="7d",
            last_done=datetime.date(2024, 1, 1),
        )

        result = task.calculate_next_due(from_date=datetime.date(2024, 1, 1))
        self.assertEqual(result, datetime.date(2024, 1, 8))

    def test_next_due_recurring_monthly(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            frequency="1m",
            last_done=datetime.date(2024, 1, 31),
        )

        result = task.calculate_next_due(from_date=datetime.date(2024, 1, 31))
        self.assertEqual(result, datetime.date(2024, 2, 29))

    def test_next_due_recurring_respects_season(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            frequency="7d",
            last_done=datetime.date(2024, 1, 1),
            all_year=False,
            seasonal_start_month=4,
            seasonal_end_month=6,
        )

        result = task.calculate_next_due(from_date=datetime.date(2024, 1, 1))
        self.assertEqual(result, datetime.date(2024, 4, 1))

    # ---------------------------------------------------------
    # MARK DONE
    # ---------------------------------------------------------

    def test_mark_done_updates_last_done_and_next_due(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            frequency="7d",
            repeat=True,
        )

        done_date = datetime.date(2024, 5, 1)
        task.mark_done(done_date)

        self.assertEqual(task.last_done, done_date)
        self.assertIsNotNone(task.next_due)
        self.assertGreater(task.next_due, done_date)

    def test_mark_done_non_repeating_deactivates_task(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            repeat=False,
        )

        task.mark_done(datetime.date(2024, 5, 1))

        self.assertFalse(task.active)
        self.assertIsNone(task.next_due)

    # ---------------------------------------------------------
    # SKIP
    # ---------------------------------------------------------

    def test_skip_moves_next_due_forward(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            frequency="7d",
            next_due=datetime.date(2024, 5, 1),
        )

        task.skip()
        self.assertEqual(task.next_due, datetime.date(2024, 5, 8))

    def test_skip_respects_season(self):
        task = PlantTask(
            plant=self.plant,
            user=self.user,
            frequency="7d",
            next_due=datetime.date(2024, 1, 1),
            all_year=False,
            seasonal_start_month=4,
            seasonal_end_month=6,
        )

        task.skip()
        self.assertEqual(task.next_due, datetime.date(2024, 4, 1))


# =========================================================
# NEW TESTS — DUPLICATE BED NAME VALIDATION
# =========================================================

class GardenBedModelTests(TestCase):
    """Ensure DB-level uniqueness constraint works."""

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")

    def test_duplicate_bed_name_raises_integrity_error(self):
        GardenBed.objects.create(owner=self.user, name="Herbs")

        with self.assertRaises(IntegrityError):
            GardenBed.objects.create(owner=self.user, name="herbs")


class GardenBedCreateViewTests(TestCase):
    """Ensure the CreateView shows a clean form error instead of crashing."""

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.client.login(username="mark", password="pass")
        GardenBed.objects.create(owner=self.user, name="Herbs")

    def test_duplicate_bed_name_shows_form_error(self):
        response = self.client.post(
            reverse("bed_create"),
            {"name": "herbs", "location": ""}
        )

        # Should re-render the form, not redirect
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIn(
            "You already have a bed with this name.",
            form.errors["name"]
        )

        # Still only one bed
        self.assertEqual(
            GardenBed.objects.filter(owner=self.user).count(),
            1
        )
