"""
Authentication tests for the accounts app.

Covers:
- Attempting to bypass login page
- Login page rendering
- Successful login
- Failed login attempts
- User registration
- Access control for protected views
"""

from django.test import TestCase
from unittest import skip
from django.urls import reverse
from django.contrib.auth.models import User
# from dotenv import load_dotenv


class AuthTests(TestCase):
    """Test suite for authentication-related views."""

    def setUp(self):
        """Create a test user used across multiple tests."""
        self.user = User.objects.create_user(
            username="mark",
            password="testpass123"
        )

    # ================== login page rendering correctly ==================
    def test_login_page_loads(self):
        """The login page should return HTTP 200 and use correct template."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    # ================== Successful login ==================
    def test_user_can_login(self):
        """A valid username/password should authenticate the user."""
        response = self.client.post(reverse("login"), {
            "username": "mark",
            "password": "testpass123"
        }, follow=True)

        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")

    # ================== Failed login Attempts ==================
    def test_login_fails_with_no_credentials(self):
        """No credentials should not authenticate the user."""
        response = self.client.post(reverse("login"), {
            "username": "",
            "password": ""
        })

        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertContains(response, "Invalid username or password")

    def test_login_fails_with_invalid_username(self):
        """Invalid username should not authenticate the user."""
        response = self.client.post(reverse("login"), {
            "username": "blobby",
            "password": "testpass123"
        })

        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertContains(response, "Invalid username or password")

    def test_login_fails_with_invalid_password(self):
        """Invalid password should not authenticate the user."""
        response = self.client.post(reverse("login"), {
            "username": "mark",
            "password": "testpass123!"
        })

        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertContains(response, "Invalid username or password")

    # ================== Access control for ADMIN protected views ============
    def test_protected_admin_view_redirects_if_not_logged_in(self):
        """Unauthenticated users are redirected to the admin login page."""
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)

    # ================== Access control for App protected views ==============
    @skip("Dashboard view not implemented yet")
    def test_protected_view_redirects_if_not_logged_in(self):
        """Unauthenticated users should be redirected to the login page."""
        pass

    # ================== User Registration tests ==================
    def test_registration_page_loads(self):
        """Registration page should render with the correct template."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_user_can_register_with_valid_data(self):
        """Valid registration data should create user and log them in."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "TestUser01",
                "password1": "password123!",
                "password2": "password123!",
                "email": "testuser01@test.com",
            },
            follow=True
        )

        self.assertTrue(User.objects.filter(username="TestUser01").exists())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertIn("_auth_user_id", self.client.session)

    def test_registration_fails_with_mismatched_passwords(self):
        """Registration should fail if passwords do not match."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "mark1",
                "password1": "password123!",
                "password2": "PassWord123",
                "email": "test@test.com",
            },
            follow=True
        )

        self.assertFalse(User.objects.filter(username="mark1").exists())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertContains(response, "Passwords do not match")

    def test_registration_fails_with_no_data(self):
        """Registration should fail if no data is entered."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "",
                "password1": "",
                "password2": "",
                "email": "",
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertContains(response, "Please correct the errors below.")

    def test_registration_fails_with_duplicate_username(self):
        """Registration should fail if the username already exists."""
        # The setUp() method already created a user named "mark"
        # # So we DO NOT create another one here.
        response = self.client.post(
            reverse("register"),
            {
                "username": "mark",
                "password1": "password123!",
                "password2": "password123!",
                "email": "test@test.com",
            },
            follow=True
        )
        # The error is handled successfully returning a response code 200
        self.assertEqual(response.status_code, 200)
        # The user is returned to the register.html page
        self.assertTemplateUsed(response, "accounts/register.html")
        # The error message tells the user the reason.
        self.assertContains(response, "Username already taken")
