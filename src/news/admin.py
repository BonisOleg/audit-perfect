from django.contrib import admin
from unfold.admin import ModelAdmin

from src.core.admin_mixins import TinyMceBodyMixin
from src.news.models import News


@admin.register(News)
class NewsAdmin(TinyMceBodyMixin, ModelAdmin):
    list_display = ("title", "published_at", "is_published")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt")
    date_hierarchy = "published_at"
    fieldsets = (
        ("Матеріал", {"fields": ("title", "slug", "excerpt", "body")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Публікація", {"fields": ("published_at", "is_published")}),
    )
