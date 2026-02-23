from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, *url_names):
    """
    Returns the string "active" when the current request's resolved URL name
    matches any of the provided ``url_names``.

    This tag is used in navigation templates to conditionally apply the
    Bootstrap `.active` class to the correct menu item based on the page
    the user is currently viewing.

    Parameters
    ----------
    context : dict
        The template context, which must include the current HttpRequest.
    *url_names : str
        One or more Django URL pattern names to compare against the
        current view's ``resolver_match.url_name``.

    Returns
    -------
    str
        "active" if the current URL name matches any provided name,
        otherwise an empty string.

    Usage in templates
    ------------------
    {% load navigation_tags %}
    <a class="nav-link {% active 'dashboard' %}" href="{% url 'dashboard' %}">
        Dashboard
    </a>
    """
    try:
        current = context["request"].resolver_match.url_name
    except Exception:
        return ""

    return mark_safe("active") if current in url_names else ""
