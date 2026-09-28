from django import forms
from django.contrib import admin

from src.core.admin_auth import GuardedGroupAdmin, GuardedUserAdmin  # noqa: F401
from src.core.admin_mixins import TinyMceBodyMixin
from src.core.admin_singleton import SingletonAdmin
from src.core.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("footer_blurb_uk", "footer_blurb_en", "policy_body_uk", "policy_body_en")

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name.startswith("color_"):
            kwargs["widget"] = forms.TextInput(attrs={"type": "color"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    fieldsets = (
        (
            None,
            {
                "fields": ("en_enabled",),
                "description": "Вимкнена англійська зникає з перемикача, а /en/ відкриває українську сторінку.",
            },
        ),
        (
            "Спільне",
            {
                "classes": ["tab"],
                "fields": (
                    "edrpou",
                    "phone",
                    "phone_href",
                    "phone_secondary",
                    "phone_secondary_href",
                    "telegram",
                    "email",
                    "map_embed_url",
                    "maps_url",
                    "registry_number",
                    "registry_url",
                    "color_red",
                    "color_blue",
                    "color_ink",
                    "color_bg",
                    "color_wash",
                    "font_display",
                    "font_body",
                ),
            },
        ),
        (
            "Українська",
            {
                "classes": ["tab"],
                "fields": (
                    "site_name_uk",
                    "tagline_uk",
                    "legal_name_uk",
                    "address_uk",
                    "hours_weekdays_uk",
                    "hours_weekend_uk",
                    "hours_note_uk",
                    "visit_directions_uk",
                    "footer_blurb_uk",
                    "consult_kicker_uk",
                    "consult_title_uk",
                    "policy_body_uk",
                    "default_meta_title_uk",
                    "default_meta_description_uk",
                    "home_meta_title_uk",
                    "home_meta_description_uk",
                    "about_meta_title_uk",
                    "about_meta_description_uk",
                    "contacts_meta_title_uk",
                    "contacts_meta_description_uk",
                    "policy_meta_title_uk",
                    "policy_meta_description_uk",
                    "services_meta_title_uk",
                    "services_meta_description_uk",
                    "news_meta_title_uk",
                    "news_meta_description_uk",
                ),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": (
                    "site_name_en",
                    "tagline_en",
                    "legal_name_en",
                    "address_en",
                    "hours_weekdays_en",
                    "hours_weekend_en",
                    "hours_note_en",
                    "visit_directions_en",
                    "footer_blurb_en",
                    "consult_kicker_en",
                    "consult_title_en",
                    "policy_body_en",
                    "default_meta_title_en",
                    "default_meta_description_en",
                    "home_meta_title_en",
                    "home_meta_description_en",
                    "about_meta_title_en",
                    "about_meta_description_en",
                    "contacts_meta_title_en",
                    "contacts_meta_description_en",
                    "policy_meta_title_en",
                    "policy_meta_description_en",
                    "services_meta_title_en",
                    "services_meta_description_en",
                    "news_meta_title_en",
                    "news_meta_description_en",
                ),
            },
        ),
    )
