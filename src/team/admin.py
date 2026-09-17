from unfold.admin import TabularInline

from src.team.models import Case, TeamMember


class TeamMemberInline(TabularInline):
    model = TeamMember
    extra = 0
    fields = ("name", "role", "photo", "sort_order", "is_active")
    ordering = ("sort_order", "name")


class CaseInline(TabularInline):
    model = Case
    extra = 0
    fields = ("title", "industry", "result", "sort_order", "is_active")
    ordering = ("sort_order", "title")
