from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import datetime


class CalendarViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="mark", password="pass")
        self.today = datetime.date.today()

    # ---------------------------------------------------------
    # HOME VIEW
    # ---------------------------------------------------------

    def test_home_is_public(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    # ---------------------------------------------------------
    # DASHBOARD LOGIN
    # ---------------------------------------------------------

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_dashboard_loads_for_logged_in_user(self):
        self.client.login(username="mark", password="pass")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")

        # Must always include selected_month/year
        self.assertIn("selected_month", response.context)
        self.assertIn("selected_year", response.context)

    # ---------------------------------------------------------
    # VALID MONTH/YEAR
    # ---------------------------------------------------------

    def test_dashboard_accepts_valid_future_month_and_year(self):
        self.client.login(username="mark", password="pass")

        # Choose a future month
        future_year = self.today.year + 1
        response = self.client.get(
            reverse("dashboard") + f"?month=4&year={future_year}"
        )

        self.assertEqual(response.context["selected_month"], 4)
        self.assertEqual(response.context["selected_year"], future_year)

    # ---------------------------------------------------------
    # INVALID MONTH/YEAR → SNAP BACK TO TODAY
    # ---------------------------------------------------------

    def test_invalid_month_defaults_to_today(self):
        self.client.login(username="mark", password="pass")

        response = self.client.get(
            reverse("dashboard") + "?month=99&year=2025"
        )

        self.assertEqual(response.context["selected_month"], self.today.month)
        self.assertEqual(response.context["selected_year"], self.today.year)

    def test_invalid_year_defaults_to_today(self):
        self.client.login(username="mark", password="pass")

        response = self.client.get(
            reverse("dashboard") + "?month=5&year=abcd"
        )

        self.assertEqual(response.context["selected_month"], self.today.month)
        self.assertEqual(response.context["selected_year"], self.today.year)

    # ---------------------------------------------------------
    # PAST MONTH/YEAR → SNAP BACK TO TODAY
    # ---------------------------------------------------------

    def test_past_month_snaps_back_to_today(self):
        self.client.login(username="mark", password="pass")

        past_year = self.today.year - 2
        response = self.client.get(
            reverse("dashboard") + f"?month=1&year={past_year}"
        )

        self.assertEqual(response.context["selected_month"], self.today.month)
        self.assertEqual(response.context["selected_year"], self.today.year)
