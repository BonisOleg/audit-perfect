from django.contrib import admin
from unfold.admin import ModelAdmin

from src.services.models import Service


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ("title", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description")
