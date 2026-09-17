from django.contrib import admin
from unfold.admin import ModelAdmin

from src.team.models import Case, TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ("name", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name", "role")


@admin.register(Case)
class CaseAdmin(ModelAdmin):
    list_display = ("title", "industry", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    search_fields = ("title", "industry")
