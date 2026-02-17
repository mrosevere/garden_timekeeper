"""
Views for the core app, including homepage rendering, dashboard access,
and CRUD operations for garden beds and plants.

These views provide the main user-facing functionality of the Garden
Timekeeper application and enforce per-user data ownership to ensure
privacy and personalised garden management.
"""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.http import JsonResponse


from datetime import date
from calendar import monthrange

from .models import GardenBed, Plant, PlantLifespan, PlantType, PlantTask
from .forms import GardenBedForm, PlantForm, PlantTaskForm


# ================= Homepage Views =======================

def home(request):
    """
    Render the public homepage for the Garden Timekeeper application.

    This view introduces the app and provides navigation to registration
    and login pages. It is accessible to both authenticated and anonymous
    users.
    """
    return render(request, 'core/home.html')


# ================= Dashboard Views =======================


@login_required
def dashboard(request):
    """
    Dashboard: Month view (default).
    Shows all tasks with next_due <= end_of_selected_month.
    Overdue tasks are those with next_due < start_of_selected_month.
    Supports sorting and forward-only month navigation.
    """

    today = date.today()

    # -----------------------------
    # 1. VIEW MODE (month only for now)
    # -----------------------------
    view_mode = request.GET.get("view", "month")

    # -----------------------------
    # 2. SELECTED MONTH
    # -----------------------------
    selected_year = request.GET.get("year")
    selected_month = request.GET.get("month")

    if selected_year and selected_month:
        try:
            year = int(selected_year)
            month = int(selected_month)
        except ValueError:
            year, month = today.year, today.month
    else:
        year, month = today.year, today.month

    # -----------------------------
    # 2b. MONTH BOUNDARIES
    # -----------------------------
    start_of_month = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_of_month = date(year, month, last_day)

    # -----------------------------
    # 2c. MONTH LABEL
    # -----------------------------
    month_label = date(year, month, 1)

    # -----------------------------
    # 2d. NEXT MONTH / NEXT YEAR
    # -----------------------------
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # -----------------------------
    # 2e. PREVIOUS MONTH / NEXT YEAR
    # -----------------------------
    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    # -----------------------------
    # 2f. Prevent navigating backwards
    # -----------------------------
    if (year, month) < (today.year, today.month):
        year, month = today.year, today.month

    # -----------------------------
    # 3. SORTING
    # -----------------------------
    sort = request.GET.get("sort", "due")
    direction = request.GET.get("direction", "asc")

    sort_options = {
        "name": "name",
        "plant": "plant__name",
        "bed": "plant__bed__name",
        "due": "next_due",
        "frequency": "frequency",
    }

    sort_field = sort_options.get(sort, "next_due")

    if direction == "desc":
        sort_field = f"-{sort_field}"

    # -----------------------------
    # 4. QUERYSET
    # Filter by user
    # -----------------------------
    tasks = (
        PlantTask.objects
        .select_related("plant", "plant__bed")
        # required to fix issue-118
        .filter(plant__owner=request.user)
        .filter(next_due__lte=end_of_month)
        .order_by(sort_field)
    )

    # -----------------------------
    # 4b. Hide overdue tasks checkbox
    # -----------------------------
    hide_overdue = request.GET.get("hide_overdue") == "1"
    if hide_overdue:
        tasks = tasks.filter(next_due__gte=start_of_month)

    # -----------------------------
    # 5. CONTEXT
    # -----------------------------
    context = {
        "tasks": tasks,
        "view_mode": view_mode,
        "month_label": month_label,
        "hide_overdue": hide_overdue,


        # navigation
        "today": today,
        "selected_year": year,
        "selected_month": month,
        "start_of_month": start_of_month,
        "end_of_month": end_of_month,
        "next_month": next_month,
        "next_year": next_year,
        "previous_month": previous_month,
        "previous_year": previous_year,

        # Sorting
        "current_sort": sort,
        "current_direction": direction,
    }

    return render(request, "core/dashboard.html", context)


# ================= Garden Bed Views =======================


class BedListView(LoginRequiredMixin, ListView):
    """
    Displays all GardenBed objects belonging to the logged‑in user.

    This view powers the main "Your Garden Beds" page and supports:
      - Per‑user data isolation
      - Searching
      - Filtering
      - Sorting
      - Pagination

    It uses Django's ListView, but overrides get_queryset() to apply
    user‑specific filtering and dynamic query modifications based on
    GET parameters.

    This keeps the view clean, predictable, and easy to extend.
    """

    model = GardenBed
    template_name = "core/beds/bed_list.html"
    paginate_by = 3  # Small page size for mobile‑friendly UX

    def get_queryset(self):
        """
        Build the queryset dynamically based on user input.

        The order of operations is intentional:

        1. Start with only the beds owned by the logged‑in user.
        2. Apply a default sort (alphabetical by name).
        3. Apply optional filters:
             - search by partial name match
             - filter by exact location
        4. Apply optional sorting, but only if the requested sort
           field is in the allowed list (prevents unsafe ordering).

        This pattern ensures:
          - predictable behaviour
          - no cross‑user data leakage
          - safe, validated sorting
          - clean, readable logic
        """

        # Step 1: User‑scoped base queryset
        qs = GardenBed.objects.filter(owner=self.request.user)

        # Step 2: Default ordering
        qs = qs.order_by("name")

        # -------------------------
        # Filtering: Search by name
        # -------------------------
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(name__icontains=search)

        # -------------------------
        # Filtering: Location
        # -------------------------
        location = self.request.GET.get("location")
        if location:
            qs = qs.filter(location=location)

        # -------------------------
        # Sorting (validated)
        # -------------------------
        allowed_sorts = [
            "name", "-name",
            "location", "-location",
            "created_at", "-created_at",
        ]

        sort = self.request.GET.get("sort")
        if sort in allowed_sorts:
            qs = qs.order_by(sort)

        return qs


class BedDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detailed information for a single GardenBed.

    This view uses Django's DetailView, but with an important security
    constraint: users may ONLY view beds that they personally own:
      - Garden beds are user‑specific data.
      - Without scoping the queryset, a user could guess another bed's ID
        (e.g., /beds/5/) and access someone else's data.
      - By overriding get_queryset(), we enforce per‑user isolation at
        the database level, not just in the template.

    If the requested bed does not belong to the logged‑in user, Django
    automatically raises a 404 — not a permission error — which avoids
    leaking the existence of other users' beds.
    """

    model = GardenBed
    template_name = "core/beds/bed_detail.html"

    # Use a clear, explicit context name instead of the default "object"
    context_object_name = "bed"

    def get_queryset(self):
        """
        Restrict the queryset to only the beds owned by the current user.

        This ensures:
          - No cross‑user data exposure
          - DetailView will 404 automatically if the bed is not found
            *within this restricted queryset*
          - The logic stays consistent with BedListView and BedUpdateView

        """
        return GardenBed.objects.filter(owner=self.request.user)


class BedCreateView(LoginRequiredMixin, CreateView):
    """
    Handles creation of a new GardenBed.

    This view supports TWO workflows:

    1. **AJAX modal submission**
       - Triggered when the user clicks “Add new bed”
        inside the Plant Create/Edit pages.
       - The modal form submits via fetch() with the header:
             X-Requested-With: XMLHttpRequest
       - Instead of redirecting, we return JSON so the page does NOT reload.
       - The JS then updates the bed dropdown and closes the modal.

    2. **Normal page submission**
       - Triggered when the user visits /beds/create/ directly.
       - The form behaves like a standard Django CreateView.
       - After saving, the user is redirected to the Beds List page.

    This dual behaviour allows the same view to power both:
       - Inline modal creation
       - Full-page creation
    without duplicating logic.
    """

    model = GardenBed
    form_class = GardenBedForm
    template_name = "core/bed_create.html"
    success_url = reverse_lazy("bed_list")  # Used ONLY for non-AJAX fallback

    def form_valid(self, form):
        """
        Called when the form is valid.

        We attach the logged-in user as the bed owner, then decide whether
        to return JSON (AJAX modal) or redirect (normal form).
        """
        form.instance.owner = self.request.user
        self.object = form.save()

        # Detect AJAX request from the modal workflow
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            # Return JSON so the page does NOT reload
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "name": self.object.name,
            })

        # Fallback: normal form submission (full page)
        messages.success(self.request, "New bed created successfully.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        """
        Handles invalid form submissions.

        AJAX:
            - Return JSON with errors so the modal can display them
              without reloading the page.

        Normal:
            - Render the template with errors as usual.
        """
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": form.errors,
            }, status=400)

        return super().form_invalid(form)


class BedUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows the logged‑in user to edit one of their existing GardenBeds.

    This view uses Django's UpdateView to handle:
      - form rendering
      - validation
      - saving changes

      • The queryset is restricted to the current user's beds to prevent
        cross‑user access (same pattern as BedDetailView and BedListView).
      • Duplicate bed names are caught at the database level (IntegrityError)
        and surfaced as a user‑friendly form error.
      • On success, the user is redirected back to the bed list.
    """

    model = GardenBed
    form_class = GardenBedForm
    template_name = "core/beds/bed_edit.html"
    success_url = reverse_lazy("bed_list")
    context_object_name = "bed"

    def get_queryset(self):
        """
        Restrict the queryset to beds owned by the logged‑in user.

        This ensures:
          - Users cannot edit beds they do not own.
          - If a user tries to access /beds/<id>/edit/ for a bed that
            isn't theirs, Django will automatically raise a 404.
        """
        return GardenBed.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        """
        Attempt to save the updated bed.

        If the user tries to rename a bed to a name they already use,
        the database will raise an IntegrityError (due to a unique
        constraint on name + owner). We catch that and convert it into
        a clean form error instead of crashing.

        This keeps the UX smooth and avoids exposing internal errors.
        """
        try:
            return super().form_valid(form)

        except IntegrityError:
            # Add a user‑friendly error message to the "name" field
            form.add_error("name", "You already have a bed with this name.")
            return self.form_invalid(form)


@login_required
def bed_delete(request, pk):
    """
    Delete a garden bed belonging to the logged-in user.

    This function-based view is intentionally retained instead of using
    Django's DeleteView so that the existing modal-based confirmation
    workflow can be preserved. The delete confirmation is rendered within
    the bed_detail template using `delete_mode`, allowing the modal to
    appear without requiring a separate confirmation page.

    On POST:
        - Permanently delete the bed and redirect to the bed list.

    On GET:
        - Render the bed detail page with delete mode enabled so the
          modal confirmation can be displayed.
    """
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)

    if request.method == "POST":
        bed.delete()
        messages.success(request, "Bed deleted successfully.")
        return redirect("bed_list")

    return render(request, "core/beds/bed_detail.html", {
        "bed": bed,
        "delete_mode": True
    })


# ================= Plant Views =======================

class PlantListView(LoginRequiredMixin, ListView):
    """
    Displays all Plant objects belonging to the logged‑in user.

    This view powers the main "Your Plants" page and supports:
      • Per‑user data isolation
      • Searching
      • Filtering (lifespan, type, bed)
      • Sorting
      • Pagination

    The structure mirrors BedListView for consistency, but with
    plant‑specific filters and sorting options.
    """

    model = Plant
    template_name = "core/plants/plant_list.html"
    paginate_by = 3  # Mobile‑friendly page size

    def get_queryset(self):
        """
        Build the queryset dynamically based on user input.

        The order of operations is intentional:

        1. Start with only the plants owned by the logged‑in user.
        2. Apply a default sort (alphabetical by name).
        3. Apply optional filters:
             - lifespan
             - type
             - bed
             - partial name search
        4. Apply optional sorting, but only if the requested sort
           field is in the allowed list (prevents unsafe ordering).

        This pattern ensures:
          • predictable behaviour
          • no cross‑user data leakage
          • safe, validated sorting
          • clean, readable logic
        """

        # Step 1: User‑scoped base queryset
        qs = Plant.objects.filter(owner=self.request.user)

        # Step 2: Default ordering
        qs = qs.order_by("name")

        # -------------------------
        # Filtering: Lifespan
        # -------------------------
        lifespan = self.request.GET.get("lifespan")
        if lifespan:
            qs = qs.filter(lifespan=lifespan)

        # -------------------------
        # Filtering: Plant type
        # -------------------------
        plant_type = self.request.GET.get("type")
        if plant_type:
            qs = qs.filter(type=plant_type)

        # -------------------------
        # Filtering: Bed
        # -------------------------
        bed_id = self.request.GET.get("bed")
        if bed_id:
            qs = qs.filter(bed_id=bed_id)

        # -------------------------
        # Filtering: Search by name
        # -------------------------
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(name__icontains=search)

        # -------------------------
        # Sorting (validated)
        # -------------------------
        allowed_sorts = [
            "name", "-name",
            "planting_date", "-planting_date",
            "type", "-type",
            "lifespan", "-lifespan",
            "bed__name", "-bed__name",
        ]

        sort = self.request.GET.get("sort")
        if sort in allowed_sorts:
            qs = qs.order_by(sort)

        return qs

    def get_context_data(self, **kwargs):
        """
        Add extra context needed for filter dropdowns.

        These choices come from the PlantLifespan and PlantType enums,
        ensuring the template always receives the canonical values.
        """
        context = super().get_context_data(**kwargs)
        context["lifespan_choices"] = PlantLifespan.choices
        context["type_choices"] = PlantType.choices
        return context


class PlantDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information for a single plant.

    The view restricts access to beds owned by the logged-in user,
    raising a 404 if the requested bed does not belong to them.
    """
    model = Plant
    template_name = "core/plants/plant_detail.html"
    context_object_name = "plant"

    def get_queryset(self):
        """
        Returns query set
        """
        return Plant.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Adds context data for view logic

        The context data is used to check whether a task is in season.
        """
        context = super().get_context_data(**kwargs)
        plant = context["plant"]

        today = date.today()

        # Precompute seasonal status for each task
        task_info = []
        for task in plant.tasks.all():
            overdue = task.is_overdue()
            days_until = task.days_until_due()
            due_soon = days_until is not None and days_until <= 3

            task_info.append({
                "task": task,
                "in_season": task.is_in_season(today),
                "overdue": overdue,
                "due_soon": due_soon,
            })

        # Sort order:
        # 1. Overdue
        # 2. Due soon
        # 3. Everything else
        task_info.sort(
            key=lambda x: (
                not x["overdue"],  # overdue first
                not x["due_soon"],  # then due soon
                x["task"].next_due or date.max  # then by date
                ))
        context["task_info"] = task_info
        return context


class PlantCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new plant for the logged-in user.

    This view renders the plant creation form and supports inline creation
    of GardenBed objects via a Bootstrap modal. The modal submits via AJAX,
    so this view does not need to handle any redirect or session logic
    related to bed creation.

    Responsibilities:
    - Render the plant form
    - Assign the logged-in user as the plant owner
    - Handle duplicate plant names gracefully
    - Provide an empty GardenBedForm to the template for the modal
    """
    model = Plant
    form_class = PlantForm
    template_name = "core/plants/plant_create.html"
    success_url = reverse_lazy("plant_list")

    def form_valid(self, form):
        """
        Assign the logged-in user as the plant owner and handle duplicate
        plant names. This method behaves exactly like a normal CreateView
        except for the duplicate-name handling.
        """
        form.instance.owner = self.request.user

        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "You already have a plant with this name.")
            return self.form_invalid(form)

        messages.success(self.request, "Plant created successfully.")
        return response

    def get_form_kwargs(self):
        """
        Inject the logged-in user into the form so that the 'bed' field
        can be filtered to only show beds owned by that user.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add an empty GardenBedForm to the context so the template can
        render the 'Create Bed' modal. The modal is submitted via AJAX,
        so no additional view logic is required here.
        """
        context = super().get_context_data(**kwargs)
        context["bed_form"] = GardenBedForm()
        return context


class PlantUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows the logged‑in user to edit one of their existing Plants.

    This view uses Django's UpdateView to handle:
      • form rendering
      • validation
      • saving changes

      • The queryset is restricted to the current user's plants to prevent
        cross‑user access (same pattern as all other Plant/Bed views).
      • Duplicate plant names (per user) are caught at the database level
        and converted into clean form errors.
      • The form receives the logged‑in user via get_form_kwargs(), allowing
        PlantForm to filter the 'bed' dropdown to only show the user's beds.
      • The modal “Create Bed” workflow is supported by injecting a fresh
        GardenBedForm into the context.
    """

    model = Plant
    form_class = PlantForm
    template_name = "core/plants/plant_edit.html"
    context_object_name = "plant"
    success_url = reverse_lazy("plant_list")

    def get_queryset(self):
        """
        Restrict the queryset to plants owned by the logged‑in user.

        This ensures:
          • Users cannot edit plants they do not own.
          • If a user tries to access /plants/<id>/edit/ for a plant that
            isn't theirs, Django will automatically raise a 404.
        """
        return Plant.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        """
        Attempt to save the updated plant.

        Behaviour:
          • On success, a confirmation message is shown.
          • If the user attempts to rename the plant to a name they already
            use, the database raises IntegrityError (due to a unique
            constraint on name + owner). We catch this and convert it into
            a user‑friendly form error.

        This avoids exposing internal errors and keeps the UX smooth.
        """
        messages.success(self.request, "Plant updated successfully.")

        try:
            return super().form_valid(form)

        except IntegrityError:
            # Add a user‑friendly error message to the "name" field
            form.add_error("name", "You already have a plant with this name.")
            return self.form_invalid(form)

    def get_form_kwargs(self):
        """
        Extend default form kwargs to include the logged‑in user.
        
          • PlantForm uses the 'user' kwarg to filter the 'bed' dropdown.
          • This ensures users can only assign plants to their own beds.
          • Prevents cross‑user data leakage through form choices.

        This pattern keeps the form logic clean and reusable.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add a fresh GardenBedForm to the context.

        This enables the inline “Create Bed” modal on the Plant Edit page.
        The modal uses this form to create a new bed via AJAX without
        leaving the page.

        Keeping this logic here (rather than in the template) keeps the
        template clean and maintains separation of concerns.
        """
        context = super().get_context_data(**kwargs)
        context["bed_form"] = GardenBedForm()
        return context


@login_required
def plant_delete(request, pk):
    """
    Delete a plant belonging to the logged-in user.

    This function-based view is intentionally retained instead of using
    Django's DeleteView so that the existing modal-based confirmation
    workflow can be preserved. The delete confirmation is rendered within
    the bed_detail template using `delete_mode`, allowing the modal to
    appear without requiring a separate confirmation page.

    On POST:
        - Permanently delete the bed and redirect to the bed list.

    On GET:
        - Render the bed detail page with delete mode enabled so the
          modal confirmation can be displayed.
    """
    plant = get_object_or_404(Plant, pk=pk, owner=request.user)

    if request.method == "POST":
        plant.delete()
        messages.success(request, "Plant deleted successfully.")
        return redirect("plant_list")

    return render(request, "core/plants/plant_detail.html", {
        "plant": plant,
        "delete_mode": True,
    })


# ================= Task Views =======================
@login_required
def task_create(request, plant_id):
    """
    Create a new task for the selected plant.
    Ensures the task belongs to the logged-in user.
    """
    plant = get_object_or_404(Plant, id=plant_id, owner=request.user)

    if request.method == "POST":
        form = PlantTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.plant = plant
            # REQUIRED for per-user ownership (issue-118)
            task.user = request.user
            task.next_due = task.calculate_next_due()
            task.save()
            return redirect("plant_detail", pk=plant.id)
    else:
        form = PlantTaskForm()

    return render(request, "core/tasks/task_form.html", {
        "form": form,
        "plant": plant,
        "title": "Create Task"
    })


@login_required
def task_delete(request, task_id):
    """
    Delete a task for the selected plant
    """
    task = get_object_or_404(PlantTask, id=task_id, plant__owner=request.user)

    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect("plant_detail", pk=task.plant.id)

    return redirect("plant_detail", pk=task.plant.id)


@login_required
def task_mark_done(request, task_id):
    """
    Mark the task as done and return to the dashboard.
    """
    task = get_object_or_404(
        PlantTask,
        id=task_id,
        plant__owner=request.user
    )

    task.mark_done()
    task.save()

    messages.success(request, f"Task '{task.name}' marked as done.")

    return redirect("dashboard")


@login_required
def task_skip(request, task_id):
    """
    Mark the task as skipped.

    This allows the user to remove the task from their dashboard
    without having to actually mark the task as done.
    """
    task = get_object_or_404(PlantTask, id=task_id, plant__owner=request.user)
    task.skip()
    task.save()
    return redirect("plant_detail")


@login_required
def task_update(request, task_id):
    """
    Edit an existing task belonging to the logged-in user.
    Recalculates next_due when frequency or seasonal window changes.
    """
    task = get_object_or_404(PlantTask, id=task_id, plant__owner=request.user)

    if request.method == "POST":
        form = PlantTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.next_due = task.calculate_next_due()
            task.save()
            messages.success(request, "Task updated successfully.")
            return redirect("plant_detail", pk=task.plant.id)
    else:
        form = PlantTaskForm(instance=task)

    return render(request, "core/tasks/task_form.html", {
        "form": form,
        "task": task,
        "plant": task.plant,
        "title": "Edit Task"
    })


class TaskDetailView(DetailView):
    """
    Task detail view to display the task information to the user

    Does not need a return as it uses the Django DetailView
    """
    model = PlantTask
    template_name = "core/tasks/task_detail.html"
    context_object_name = "task"


class CustomLoginView(LoginView):
    """
    Extends Django's built‑in LoginView to support a 'Remember me' option.

    Background:
      • By default, Django's session cookie persists even after the browser
        is closed — it only expires when SESSION_COOKIE_AGE is reached
        (2 weeks by default).
      • This behaviour does NOT match user expectations when a login form
        includes a 'Remember me' checkbox.

    Goal:
      • If the user does NOT tick 'Remember me':
            → Session expires when the browser closes (expiry = 0)
      • If the user DOES tick 'Remember me':
            → Session persists for Django's normal duration

    This override ensures the login behaviour aligns with the semantics
    of the checkbox and provides a familiar, intuitive UX.
    """

    def form_valid(self, form):
        """
        Called when the login form is successfully validated.

        We inspect the POST data to determine whether the user selected
        'Remember me', and adjust the session expiry accordingly.
          • Django stores session expiry per‑session, not globally.
          • set_expiry(0) → session cookie becomes a browser‑session cookie.
          • set_expiry(seconds) → persistent cookie for that duration.

        This keeps the logic simple, explicit, and fully aligned with
        Django's session framework.
        """
        remember_me = self.request.POST.get('remember_me')

        if not remember_me:
            # User did NOT tick 'Remember me':
            # → Expire the session when the browser closes.
            self.request.session.set_expiry(0)
        else:
            # User DID tick 'Remember me':
            # → Keep the session for Django's default duration (2 weeks).
            #   1209600 seconds = 14 days.
            self.request.session.set_expiry(1209600)

        return super().form_valid(form)
