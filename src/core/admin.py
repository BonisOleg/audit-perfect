from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from unfold.admin import ModelAdmin

from src.core.models import SiteBlock, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        (
            "Бренд",
            {"fields": ("site_name", "tagline", "legal_name", "edrpou")},
        ),
        (
            "Контакти",
            {
                "fields": (
                    "phone",
                    "phone_href",
                    "phone_secondary",
                    "phone_secondary_href",
                    "telegram",
                    "email",
                    "address",
                    "map_embed_url",
                    "maps_url",
                )
            },
        ),
        (
            "Візит",
            {
                "fields": (
                    "hours_weekdays",
                    "hours_weekend",
                    "hours_note",
                    "visit_directions",
                )
            },
        ),
        (
            "Реєстр",
            {"fields": ("registry_number", "registry_url")},
        ),
        (
            "SEO",
            {"fields": ("default_meta_title", "default_meta_description")},
        ),
    )

    def has_add_permission(self, request) -> bool:
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = SiteSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse("admin:core_sitesettings_change", args=[obj.pk])
        )


@admin.register(SiteBlock)
class SiteBlockAdmin(ModelAdmin):
    list_display = ("page", "key", "title", "is_visible", "sort_order")
    list_filter = ("page", "is_visible", "block_type")
    search_fields = ("key", "title", "body")
    ordering = ("page", "sort_order", "key")
