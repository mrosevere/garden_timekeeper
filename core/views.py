"""
Views for the core app, including homepage rendering, dashboard access,
and CRUD operations for garden beds and plants.

These views provide the main user-facing functionality of the Garden
Timekeeper application and enforce per-user data ownership to ensure
privacy and personalised garden management.
"""

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.contrib import messages

from datetime import date

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
    Display the main dashboard for authenticated users.
    Shows all tasks ordered by next due date.
    """
    tasks = PlantTask.objects.select_related(
        "plant", "plant__bed").order_by("next_due")

    context = {"tasks": tasks, }

    return render(request, "core/dashboard.html", context)


# ================= Garden Bed Views =======================


class BedListView(LoginRequiredMixin, ListView):
    """
    Display a list of garden beds belonging to the logged-in user.

    This view uses Django's ListView to retrieve and render only the
    beds owned by the current user, ensuring per-user data isolation.
    """
    model = GardenBed
    template_name = "core/beds/bed_list.html"
    paginate_by = 3

    def get_queryset(self):
        qs = GardenBed.objects.filter(owner=self.request.user)

        # Default sort
        qs = qs.order_by("name")

        # == Filtering ==
        # Search by name (partial match)
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(name__icontains=search)

        # Filter by location
        location = self.request.GET.get("location")
        if location:
            qs = qs.filter(location=location)

        # Sorting
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
    Display detailed information for a single garden bed.

    The view restricts access to beds owned by the logged-in user,
    raising a 404 if the requested bed does not belong to them.
    """
    model = GardenBed
    template_name = "core/beds/bed_detail.html"
    # Set context rather than using default object_list / gardenbed_list
    context_object_name = "bed"

    def get_queryset(self):
        return GardenBed.objects.filter(owner=self.request.user)


class BedCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new garden bed for the logged-in user.

    Django's CreateView handles form display, validation, and saving.
    The logged-in user is automatically assigned as the bed owner
    before the object is saved. Duplicate names are caught and
    surfaced as form errors.
    """
    model = GardenBed
    form_class = GardenBedForm
    template_name = "core/beds/bed_create.html"
    success_url = reverse_lazy("bed_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "You already have a bed with this name.")
            return self.form_invalid(form)

        # Success message (for creating via modal)
        messages.success(self.request, "New bed created successfully.")

        # next for inline modal creation
        next_url = self.request.POST.get("next")
        if next_url:
            return redirect(next_url)

        return response


class BedUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit an existing garden bed belonging to the logged-in user.

    This view reuses Django's UpdateView to handle form rendering and
    validation. Duplicate names are caught and surfaced as form errors.
    """
    model = GardenBed
    form_class = GardenBedForm
    template_name = "core/beds/bed_edit.html"
    success_url = reverse_lazy("bed_list")
    context_object_name = "bed"

    def get_queryset(self):
        return GardenBed.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
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
    Display a list of plants belonging to the logged-in user.

    This view uses Django's ListView to retrieve and render only the
    plants owned by the current user, ensuring per-user data isolation.
    """
    model = Plant
    template_name = "core/plants/plant_list.html"
    paginate_by = 3

    def get_queryset(self):
        qs = Plant.objects.filter(owner=self.request.user)

        # Default sort
        qs = qs.order_by("name")

        # == Filtering ==
        # Filter by lifespan
        lifespan = self.request.GET.get("lifespan")
        if lifespan:
            qs = qs.filter(lifespan=lifespan)

        # filter by type
        plant_type = self.request.GET.get("type")
        if plant_type:
            qs = qs.filter(type=plant_type)

        # filter by bed
        bed_id = self.request.GET.get("bed")
        if bed_id:
            qs = qs.filter(bed_id=bed_id)

        # Search by name (partial match)
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(name__icontains=search)

        # Sorting
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

    Django's CreateView handles form display, validation, and saving.
    The logged-in user is automatically assigned as the plant owner
    before the object is saved. Duplicate names are caught and
    surfaced as form errors.
    """
    model = Plant
    form_class = PlantForm
    template_name = "core/plants/plant_create.html"
    success_url = reverse_lazy("plant_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # Exception handling when attempting to create a duplicate
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "You already have a plant with this name.")
            return self.form_invalid(form)

        # Success message
        messages.success(self.request, "Plant created successfully.")

        return response

    def get_form_kwargs(self):
        """
        Extend default form kwargs to include the logged-in user.

        This allows the PlantForm to filter the 'bed' queryset so that
        users can only assign plants to their own garden beds.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    # For modal create bed directly from create plant
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bed_form"] = GardenBedForm()
        return context


class PlantUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit an existing plant belonging to the logged-in user.

    This view reuses Django's UpdateView to handle form rendering and
    validation. Duplicate names are caught and surfaced as form errors.
    """
    model = Plant
    form_class = PlantForm
    template_name = "core/plants/plant_edit.html"
    context_object_name = "plant"
    success_url = reverse_lazy("plant_list")

    def get_queryset(self):
        return Plant.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        # confirmation message
        messages.success(self.request, "Plant updated successfully.")
        # exception handling for duplicate plant name
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error("name", "You already have a plant with this name.")
            return self.form_invalid(form)

    def get_form_kwargs(self):
        """
        Extend default form kwargs to include the logged-in user.

        This allows the PlantForm to filter the 'bed' queryset so that
        users can only assign plants to their own garden beds.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    # For modal create bed directly from edit plant page
    def get_context_data(self, **kwargs):
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
    Create a new task for the selected plant
    """
    plant = get_object_or_404(Plant, id=plant_id, owner=request.user)

    if request.method == "POST":
        form = PlantTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.plant = plant
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
    Mark the task as done and save it.
    """
    task = get_object_or_404(PlantTask, id=task_id, plant__owner=request.user)
    task.mark_done()
    task.save()
    return redirect("plant_detail", pk=task.plant.id)


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
    return redirect("plant_detail", pk=task.plant.id)


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
    """
    model = PlantTask
    template_name = "core/tasks/task_detail.html"
    context_object_name = "task"
