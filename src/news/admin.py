from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import TinyMceBodyMixin
from src.news.models import News


@admin.register(News)
class NewsAdmin(TinyMceBodyMixin, ModelAdmin):
    list_display = ("title_uk", "published_at", "is_published")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title_uk",)}
    search_fields = ("title_uk", "title_en", "excerpt_uk")
    date_hierarchy = "published_at"
    tinymce_fields = ("body_uk", "body_en")
    fieldsets = (
        (
            "Спільне",
            {"classes": ["tab"], "fields": ("slug", "published_at", "is_published")},
        ),
        (
            "Українська",
            {
                "classes": ["tab"],
                "fields": ("title_uk", "excerpt_uk", "body_uk", "meta_title_uk", "meta_description_uk"),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": ("title_en", "excerpt_en", "body_en", "meta_title_en", "meta_description_en"),
            },
        ),
    )
