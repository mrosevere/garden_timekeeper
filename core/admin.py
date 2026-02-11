from django.contrib import admin
from .models import Plant, GardenBed, PlantTask


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "lifespan", "bed", "owner")
    search_fields = ("name", "latin_name")
    list_filter = ("type", "lifespan", "bed")


@admin.register(GardenBed)
class GardenBedAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "created_at")
    search_fields = ("name", "location")
    list_filter = ("location",)


@admin.register(PlantTask)
class PlantTaskAdmin(admin.ModelAdmin):
    list_display = ("name", "plant", "frequency", "next_due", "active")
    search_fields = ("name", "notes")
    list_filter = ("frequency", "active", "all_year")
