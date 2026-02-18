from django import template
import calendar

register = template.Library()


@register.filter
def month_name(month_number):
    """
    Convert an integer month (1–12) into its full month name.
    Example: 2 → "February"
    """
    try:
        month_number = int(month_number)
        return calendar.month_name[month_number]
    except (ValueError, IndexError):
        return ""


@register.filter
def to(start, end):
    """
    Usage: {% for i in 1|to:12 %}
    Generates a range from start to end inclusive.
    Dashboard Page - Task navigation
    """
    try:
        start = int(start)
        end = int(end)
        return range(start, end + 1)
    except ValueError:
        return []
