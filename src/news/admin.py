from django.contrib import admin
from unfold.admin import ModelAdmin

from src.news.models import News


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ("title", "published_at", "is_published")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt")
    date_hierarchy = "published_at"
