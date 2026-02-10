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

from .models import GardenBed, Plant
from .forms import GardenBedForm, PlantForm


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

    This view will eventually summarise the user's garden activity,
    including garden beds, plants, and upcoming tasks. For now, it
    simply renders the dashboard template.
    """
    return render(request, "core/dashboard.html")


# ================= Garden Bed Views =======================


class BedListView(LoginRequiredMixin, ListView):
    """
    Display a list of garden beds belonging to the logged-in user.

    This view uses Django's ListView to retrieve and render only the
    beds owned by the current user, ensuring per-user data isolation.
    """
    model = GardenBed
    template_name = "core/beds/bed_list.html"
    # Set context rather than using default object_list / gardenbed_list
    context_object_name = "beds"

    def get_queryset(self):
        return GardenBed.objects.filter(owner=self.request.user)


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

        # This code is now reachable
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
    # Set context rather than using default object_list / plant_list
    context_object_name = "plants"

    def get_queryset(self):
        return Plant.objects.filter(owner=self.request.user)


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
        return Plant.objects.filter(owner=self.request.user)


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
        return redirect("plant_list")

    return render(request, "core/plants/plant_detail.html", {
        "plant": plant,
        "delete_mode": True,
    })
