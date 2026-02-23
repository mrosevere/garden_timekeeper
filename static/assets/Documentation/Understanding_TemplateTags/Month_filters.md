## Custom Template Filters (Month Formatting)

Django’s templating system includes a number of built‑in filters, but it does not provide convenient helpers for formatting month values or converting numeric month indices into human‑readable labels.  
To keep templates clean and expressive, the project includes a small set of custom filters for working with month values in the calendar and dashboard views.

These filters live in `core/templatetags/month_filters.py` and are automatically available once the `core` app is installed.

---

### Why custom month filters are needed

- Django does not include a built‑in filter for converting a month number (e.g., `2`) into a month name (`February`).
- Templates should remain clean and declarative — logic such as `calendar.month_name[x]` does not belong in HTML.
- The project frequently displays month labels in the calendar dropdown and task views, so a reusable filter keeps the code DRY and readable.
- Using a template filter ensures consistent formatting across the entire application.

---

### Available filters

The module provides filters such as:

- **`month_name`** — Converts a numeric month (1–12) into its full month name.
- **`month_abbr`** — Converts a numeric month into its abbreviated name (e.g., `"Feb"`).
- **`month_range`** — Returns a list of month numbers for iteration in templates.
- **`month_label`** — Formats a month number into a human‑friendly label for dropdowns.

*(Your exact filter names may vary — adjust this list to match your implementation.)*

---

### Example usage in templates

```django
{% load month_filters %}

<!-- Display a full month name -->
{{ 3|month_name }}   <!-- "March" -->

<!-- Display an abbreviated month name -->
{{ 11|month_abbr }}  <!-- "Nov" -->

<!-- Build a month dropdown -->
<select>
    {% for m in 1|month_range:12 %}
        <option value="{{ m }}">
            {{ m|month_name }}
        </option>
    {% endfor %}
</select>
```

These helpers keep templates clean and expressive, especially in the calendar navigation UI.

### Implementation (excerpt)
```Python
@register.filter
def month_name(month_number):
    """
    Converts a numeric month (1–12) into its full month name.

    Parameters
    ----------
    month_number : int
        The month index to convert.

    Returns
    -------
    str
        The full month name (e.g., "January"), or an empty string if the
        value is invalid.
    """
    try:
        return calendar.month_name[int(month_number)]
    except Exception:
        return ""
```

These filters centralise month‑related formatting logic in one place, ensuring:
- consistent display across the app
- cleaner templates
- easier maintenance
- fewer hard‑coded strings
They also make the calendar UI more readable and professional, which improves the overall user experience.
