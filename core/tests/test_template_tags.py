from django.test import SimpleTestCase, RequestFactory
from django.template import Context, Template
from core.templatetags.navigation_tags import active
from core.templatetags.month_filters import month_name, to


# ==========================================================================
# Active Tag Tests
# ==========================================================================

class ActiveTagTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def render(self, url_name, tag_args):
        """
        Helper to render a template containing the {% active %} tag.
        """
        request = self.factory.get("/")
        request.resolver_match = type("Resolver", (), {"url_name": url_name})

        template_string = (
            "{% load navigation_tags %}"
            "<a class='nav-link {% active " + tag_args + " %}'>Link</a>"
        )

        template = Template(template_string)
        return template.render(Context({"request": request}))

    def test_active_tag_matches_single_name(self):
        output = self.render("dashboard", "'dashboard'")
        self.assertIn("active", output)

    def test_active_tag_does_not_match(self):
        output = self.render("dashboard", "'home'")
        self.assertNotIn("active", output)

    def test_active_tag_matches_multiple_names(self):
        output = self.render("plants", "'home' 'plants' 'tasks'")
        self.assertIn("active", output)


# ==========================================================================
# Month Filter Tests
# ==========================================================================

class MonthFilterTests(SimpleTestCase):

    def test_month_name_valid(self):
        self.assertEqual(month_name(1), "January")
        self.assertEqual(month_name(12), "December")

    def test_month_name_invalid(self):
        self.assertEqual(month_name(0), "")
        self.assertEqual(month_name(13), "")
        self.assertEqual(month_name("x"), "")

    def test_to_valid_range(self):
        result = list(to(1, 3))
        self.assertEqual(result, [1, 2, 3])

    def test_to_invalid_range(self):
        result = list(to("x", 5))
        self.assertEqual(result, [])
