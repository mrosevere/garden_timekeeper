"""
Views for the core app, including homepage rendering, dashboard access,
and CRUD operations for garden beds and plants.

These views provide the main user-facing functionality of the Garden
Timekeeper application and enforce per-user data ownership to ensure
privacy and personalised garden management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import GardenBed, Plant
from .forms import GardenBedForm, PlantForm


def home(request):
    """
    Render the public homepage for the Garden Timekeeper application.

    This view introduces the app and provides navigation to registration
    and login pages. It is accessible to both authenticated and anonymous
    users.
    """
    return render(request, 'core/home.html')


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

@login_required
def bed_list(request):
    """
    Display a list of all garden beds belonging to the logged-in user.

    Only beds owned by the current user are shown, ensuring that users
    can view and manage only their own garden layout.
    """
    beds = GardenBed.objects.filter(owner=request.user)
    return render(request, "core/beds/bed_list.html", {"beds": beds})


@login_required
def bed_detail(request, pk):
    """
    Display detailed information for a single garden bed.

    The view ensures that the requested bed belongs to the current user.
    If the bed does not exist or is not owned by the user, a 404 error
    is raised.
    """
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)
    return render(request, "core/beds/bed_detail.html", {"bed": bed})


@login_required
def bed_create(request):
    """
    Create a new garden bed for the logged-in user.

    On POST:
        - Validate form data.
        - Assign the current user as the bed owner.
        - Handle IntegrityError if the user already has a bed with the
          same name.
    On GET:
        - Display an empty form for creating a new bed.
    """
    if request.method == "POST":
        form = GardenBedForm(request.POST)
        if form.is_valid():
            bed = form.save(commit=False)
            bed.owner = request.user
            try:
                bed.save()
                return redirect("bed_list")
            except IntegrityError:
                form.add_error(
                    "name", "You already have a bed with this name.")
    else:
        form = GardenBedForm()

    return render(request, "core/beds/bed_create.html", {"form": form})


@login_required
def bed_edit(request, pk):
    """
    Edit an existing garden bed belonging to the logged-in user.

    On POST:
        - Validate and save changes.
        - Handle IntegrityError if the updated name conflicts with an
          existing bed owned by the user.
    On GET:
        - Display the form pre-filled with the bed's current data.
    """
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)

    if request.method == "POST":
        form = GardenBedForm(request.POST, instance=bed)
        if form.is_valid():
            try:
                form.save()
                return redirect("bed_list")
            except IntegrityError:
                form.add_error(
                    "name", "You already have a bed with this name.")
    else:
        form = GardenBedForm(instance=bed)

    return render(request, "core/beds/bed_edit.html", {
        "bed": bed,
        "form": form
    })


@login_required
def bed_delete(request, pk):
    """
    Delete a garden bed belonging to the logged-in user.

    On POST:
        - Permanently delete the bed and redirect to the bed list.
    On GET:
        - Render the bed detail page in delete confirmation mode.
    """
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)

    if request.method == "POST":
        bed.delete()
        return redirect("bed_list")

    return render(request, "core/beds/bed_detail.html", {
        "bed": bed,
        "delete_mode": True
    })
