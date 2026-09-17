from django.contrib import admin

from src.core.admin_auth import GuardedGroupAdmin, GuardedUserAdmin  # noqa: F401
from src.core.admin_mixins import TinyMceBodyMixin
from src.core.admin_singleton import SingletonAdmin
from src.core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("footer_blurb",)
    fieldsets = (
        (
            "Бренд",
            {
                "fields": ("site_name", "tagline", "legal_name", "edrpou"),
                "description": "Контакти, бренд і текст футера. Пункти меню не змінюються.",
            },
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
            "Футер",
            {
                "fields": ("footer_blurb", "consult_kicker", "consult_title"),
                "description": "Пункти меню тут не змінюються.",
            },
        ),
        (
            "Реєстр",
            {"fields": ("registry_number", "registry_url"), "classes": ("collapse",)},
        ),
        (
            "SEO службових сторінок",
            {
                "classes": ("collapse",),
                "fields": (
                    "default_meta_title",
                    "default_meta_description",
                    "contacts_meta_title",
                    "contacts_meta_description",
                    "policy_meta_title",
                    "policy_meta_description",
                    "services_meta_title",
                    "services_meta_description",
                    "news_meta_title",
                    "news_meta_description",
                )
            },
        ),
    )
