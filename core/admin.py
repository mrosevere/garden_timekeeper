from django.contrib import admin
from .models import GardenBed


@admin.register(GardenBed)
class GardenBedAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "created_at")
    list_filter = ("owner",)
    search_fields = ("name", "location")
