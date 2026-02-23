## Custom Template Tags (Navigation Active State)

Django provides a powerful templating system, but it does not automatically highlight the “current page” in navigation menus. Frameworks like Bootstrap expect you to add an `.active` class to the correct `<a>` element, but Django has no built‑in mechanism to determine which link should be active.

To solve this, the project includes a small custom template tag that compares the current URL name with the names of each navigation link.

---

### Why a custom tag is needed

- **CSS alone cannot detect the current URL** — it can only style what is already in the DOM.
- **Bootstrap does not automatically highlight the active page** — it simply styles `.active` if you add it yourself.
- **Django does not add `.active` automatically** — every project structures navigation differently, so Django leaves this decision to the developer.
- **JavaScript is not ideal** — it relies on string‑matching URLs, breaks with named routes, and runs after page load.

Using a Django template tag is the cleanest, most idiomatic solution. It runs server‑side, uses Django’s URL resolver, and works reliably across all views.

---

### How the `active` tag works

The tag lives in `core/templatetags/navigation_tags.py` and is loaded into templates with:

```django
{% load navigation_tags %}
```

It compares the current request’s resolved URL name with one or more names you pass in:
```django
<a class="nav-link{% active 'dashboard' %}" href="{% url 'dashboard' %}">
    Dashboard
</a>
```

If the current page’s URL name matches "dashboard", the tag outputs " active" and Bootstrap applies the .active styling. Otherwise, it outputs an empty string.

### Implementation

```Python
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
    """
```

Example usage in the navbar
```Python
<li class="nav-item">
    <a class="nav-link{% active 'home' %}" href="{% url 'home' %}">
        Home
    </a>
</li>

<li class="nav-item">
    <a class="nav-link{% active 'dashboard' %}" href="{% url 'dashboard' %}">
        Dashboard
    </a>
</li>
```

### Styling the active link
Bootstrap 5’s default .active styling is subtle, so the project adds a clearer highlight:

```CSS
.navbar .nav-link.active {
    font-weight: 600;
    color: var(--bs-primary) !important;
    border-bottom: 2px solid var(--bs-primary);
}
```

This gives users a clear visual cue about which page they are on.