"""
Views for the core app, including homepage rendering, custom error handlers,
and any shared view logic used across the project.

These views provide the entry point to the application and support global
behaviours that are not tied to a specific feature area such as plants,
tasks, or user accounts.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GardenBed
from .forms import GardenBedForm
from django.db import IntegrityError
# from django.core.exceptions import ValidationError


def home(request):
    """
    Render the public homepage for the Garden Timekeeper application.

    This view introduces the app and provides navigation to registration
    and login pages. It is accessible to both authenticated and anonymous
    users.
    """
    return render(request, 'core/home.html')


# Dashboard is only available if user is logged in.
@login_required
def dashboard(request):
    """
    Display the main dashboard for logged in users.
    This will later show summary data (beds, plants, tasks).
    """
    return render(request, "core/dashboard.html")


# ===================================================
@login_required
def bed_list(request):
    """     """
    beds = GardenBed.objects.filter(owner=request.user)
    return render(request, "core/beds/bed_list.html", {"beds": beds})


@login_required
def bed_detail(request, pk):
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)
    return render(request, "core/beds/bed_detail.html", {"bed": bed})


# =================Bed Views ===============================
@login_required
def bed_create(request):
    """ Create new bed - check for DB integrity errors and handle them """
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
                    "name", "You already have a bed with this name."
                    )
    else:
        form = GardenBedForm()

    return render(request, "core/beds/bed_create.html", {"form": form})


@login_required
def bed_edit(request, pk):
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)

    if request.method == "POST":
        form = GardenBedForm(request.POST, instance=bed)
        if form.is_valid():
            try:
                form.save()
                return redirect("bed_list")
            except IntegrityError:
                form.add_error(
                    "name", "you already have a bed with this name."
                    )
    else:
        form = GardenBedForm(instance=bed)
    return render(request, "core/beds/bed_edit.html", {
        "bed": bed,
        "form": form
        })


@login_required
def bed_delete(request, pk):
    bed = get_object_or_404(GardenBed, pk=pk, owner=request.user)
    if request.method == "POST":
        bed.delete()
        return redirect("bed_list")

    return render(request, "core/beds/bed_detail.html", {
        "bed": bed,
        "delete_mode": True
    })
