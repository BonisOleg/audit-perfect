from unfold.admin import StackedInline

from src.team.models import Case, TeamMember


class TeamMemberInline(StackedInline):
    model = TeamMember
    extra = 0
    can_delete = True
    tab = True
    ordering = ("sort_order", "name_uk")
    fieldsets = (
        (
            "Спільне",
            {"fields": ("photo", "sort_order", "is_active")},
        ),
        (
            "Українська",
            {"fields": ("name_uk", "role_uk")},
        ),
        (
            "English",
            {"fields": ("name_en", "role_en")},
        ),
    )


class CaseInline(StackedInline):
    model = Case
    extra = 0
    can_delete = True
    tab = True
    ordering = ("sort_order", "title_uk")
    fieldsets = (
        (
            "Спільне",
            {"fields": ("sort_order", "is_active")},
        ),
        (
            "Українська",
            {"fields": ("title_uk", "industry_uk", "result_uk")},
        ),
        (
            "English",
            {"fields": ("title_en", "industry_en", "result_en")},
        ),
    )
