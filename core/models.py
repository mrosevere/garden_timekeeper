"""
The core app models
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.conf import settings
from calendar import monthrange
from datetime import date, timedelta
# from django.utils import timezone

# ================= Garden Bed Models =================


class GardenBed(models.Model):
    """
    A physical garden bed or container owned by a user.

    A GardenBed stores basic descriptive information such as its name,
    location within the garden, and an optional description. Each bed is
    associated with a specific user, enabling personalised garden layouts.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="garden_beds"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "owner",
                name="unique_bed_name_per_user_case_insensitive"
            )
        ]

    def __str__(self):
        return self.name


# ================= PLANT MODELS =================
class PlantType(models.TextChoices):
    """
    Plant type categories.

    These values classify the plant type. The stored values are short codes,
    while the human readable labels are used in forms and the admin interface.
    """
    # Constant = DBValue, Label
    VEGETABLE = "VEG", "Vegetable"
    FRUIT = "FRU", "Fruit"
    HERB = "HER", "Herb"
    FLOWER = "FLO", "Flower"
    SHRUB = "SHR", "Shrub"
    TREE = "TRE", "Tree"


class PlantLifespan(models.TextChoices):
    """
    Plant lifespan categories.

    These values classify how long a plant lives and therefore
    how it behaves in the garden. The stored values are short codes,
    while the human readable labels are used in forms and the admin interface.
    """

    # Constant = DBValue, Label
    ANNUAL = "ANN", "Annual"
    PERENNIAL = "PER", "Perennial"
    BIENNIAL = "BIE", "Biennial"


class Plant(models.Model):

    """
    Represents a plant grown by a user.

    A Plant stores botanical information such as its common name,
    optional Latin name, and lifespan classification.
    It also includes optional planting metadata and free text notes.
    Each plant is owned by a specific user,
    allowing personalised garden tracking.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plants"
    )
    name = models.CharField(max_length=100)
    latin_name = models.CharField(max_length=100, blank=True)
    lifespan = models.CharField(
        choices=PlantLifespan.choices,
        default=PlantLifespan.PERENNIAL,
    )
    type = models.CharField(
        choices=PlantType.choices,
    )
    planting_date = models.DateField(null=True, blank=True)
    # Ensure that linked Plants are NOT also deleted when a Bed is deleted.
    # Any plants linked to the deleted bed will no longer have a Bed assigned.
    # The Template modal will also warn the user.
    bed = models.ForeignKey(
        GardenBed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plants"
    )

    notes = models.TextField(blank=True)

    image = models.ImageField(upload_to="plant_images/", blank=True, null=True)

    def __str__(self):
        return self.name


# ================= TASK MODELS =================


class PlantTask(models.Model):
    """
    Represents a task assigned to a plant.

    A PlantTask stores task information such as its pruning details,
    task frequency, and seasonal windows.
    It also includes optional task metadata and free text notes.
    Each task is assigned to a specific plant, and owned by a user.

    """
    # Meta data
    class Meta:
        ordering = ["next_due", "last_done", "name"]

    # link to User
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="tasks"
        )

    # link to Plant
    plant = models.ForeignKey(
        "core.Plant",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    # Task Fields
    name = models.CharField(max_length=100)

    # Seasonal Window
    # default is all year
    all_year = models.BooleanField(
        default=True,
        help_text="If selected, this task is active all year"
    )

    # For the PlantTask Seasonal Window picker UI
    MONTH_CHOICES = [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December")
    ]

    seasonal_start_month = models.PositiveSmallIntegerField(
        choices=MONTH_CHOICES,
        default=1,
        help_text="Start month",
    )

    seasonal_end_month = models.PositiveSmallIntegerField(
        choices=MONTH_CHOICES,
        default=12,
        help_text="End month"
    )

    # Task Frequency
    TASK_FREQUENCY = [
        ("7d", "Every 7 days"),
        ("14d", "Every 14 days"),
        ("1m", "Monthly"),
        ("3m", "Quarterly"),
        ("6m", "Half-yearly"),
        ("12m", "Yearly"),
    ]

    frequency = models.CharField(
        max_length=3,
        choices=TASK_FREQUENCY,
        default="7d"
    )

    # Repeat Flag (uncheck for a one off task)
    repeat = models.BooleanField(
        default=True,
        help_text="Uncheck for a one-off task."
    )

    # WYSIWYG Notes field using Summernotes
    notes = models.TextField(blank=True)

    # Scheduling fields
    last_done = models.DateField(null=True, blank=True)
    next_due = models.DateField(null=True, blank=True)

    # Created date
    created_at = models.DateTimeField(auto_now_add=True)

    # Active flag
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.plant.name})"

    # function to check if task is currently in season (due)
    def is_in_season(self, date):
        """
        Returns a boolean True/False depending on whether
        the current month is in the season window for the
        maintenance task.

        """
        month = date.month
        if self.all_year:
            return True
        # get the season start and end dates
        start_month = self.seasonal_start_month
        end_month = self.seasonal_end_month
        # check if the start month is before the end month
        if start_month <= end_month:
            # Evaluate T/F based on if the current month is within the window
            return start_month <= month <= end_month
        # Logic to handle the seasonal window going over year end
        return month >= start_month or month <= end_month

    # function to set the task frequency as a delta
    def get_frequency_delta(self):
        """
        Returns a dictionary describing the frequency interval.
        Example:
            {"days": 7, "months": 0}
            {"days": 0, "months": 1}
        """

        freq = self.frequency

        if freq.endswith("d"):
            return {
                "days": int(freq[:-1]),
                "months": 0
            }

        if freq.endswith("m"):
            return {
                "days": 0,
                "months": int(freq[:-1])
            }

        # Fallback (should never happen)
        return {"days": 7, "months": 0}

    # Function to add months as nothing found in Django to do this.
    def add_months(self, date, months):
        """
        Adds a number of months to a date, adjusting for month length.
        """
        # temporarily re-calculate converting to zero-based index!!
        new_month = date.month - 1 + months
        # handles year rollover (eg season = December-March)
        new_year = date.year + new_month // 12
        # convert zero-based month back to calendar month.
        new_month = new_month % 12 + 1

        # create tuple of two integers: (weekday, days in month)
        last_day = monthrange(new_year, new_month)[1]
        # set the day to the last valid day of the new month (as varies)
        new_day = min(date.day, last_day)

        return date.replace(year=new_year, month=new_month, day=new_day)

    def calculate_next_due(self, from_date=None):
        """
        Calculates the next due date based on frequency and seasonal window.
        Does not save the model — just returns the calculated date.
        """
        today = date.today()

        # --- 1. Handle NEW tasks (no last_done) ---
        if self.last_done is None:
            # Case A: Today is in season
            if self.is_in_season(today):
                return today

            # Case B: Today is before the seasonal window
            start_month = self.seasonal_start_month
            end_month = self.seasonal_end_month

            if today.month < start_month:
                # Start of this year's season
                return date(today.year, start_month, 1)

            # Case C: Today is after the seasonal window
            # → next year's season
            return date(today.year + 1, start_month, 1)

        # --- 2. Handle RECURRING tasks ---
        # Determine starting point
        current = from_date or self.last_done or today

        # Apply frequency
        delta = self.get_frequency_delta()

        if delta["days"] > 0:
            next_date = current + timedelta(days=delta["days"])
        else:
            next_date = self.add_months(current, delta["months"])

        # Move forward until in season
        while not self.is_in_season(next_date):
            next_date += timedelta(days=1)

        return next_date

    def mark_done(self, done_date=None):
        """
        Marks the task as completed.
        Updates last_done and calculates the next due date if repeating.
        Does not save the model — the caller should save().
        """

        # 1. Set last_done
        self.last_done = done_date or date.today()

        # 2. If not repeating, deactivate the task
        if not self.repeat:
            self.active = False
            self.next_due = None
            return self

        # 3. Calculate next due date
        self.next_due = self.calculate_next_due(from_date=self.last_done)

        return self

    def skip(self):
        """
        Skips the current cycle.
        Moves next_due forward by one frequency interval.
        Does not modify last_done.
        Does not save the model — the caller should save().
        """

        # 1. Determine the starting point
        current = self.next_due or date.today()

        # 2. Get frequency delta
        delta = self.get_frequency_delta()

        # 3. Apply the frequency
        if delta["days"] > 0:
            next_date = current + timedelta(days=delta["days"])
        else:
            next_date = self.add_months(current, delta["months"])

        # 4. Adjust for seasonal window
        while not self.is_in_season(next_date):
            next_date += timedelta(days=1)

        # 5. Update the task
        self.next_due = next_date

        return self

    def is_overdue(self):
        """
        Returns True if the task is overdue.
        """
        return self.next_due and self.next_due < date.today()

    def days_until_due(self):
        """
        Returns number of days until the task is next due
        """
        return (self.next_due - date.today()).days if self.next_due else None
