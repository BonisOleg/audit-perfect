from django.contrib import admin
from unfold.admin import StackedInline

from src.core.admin_mixins import TinyMceBodyMixin
from src.core.admin_singleton import SingletonAdmin
from src.pages.models import AboutPage, Certificate, HomePage
from src.team.admin import CaseInline, TeamMemberInline


class CertificateInline(StackedInline):
    model = Certificate
    extra = 1
    fields = ("title", "image", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(HomePage)
class HomePageAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("hero_title", "hero_lead")
    fieldsets = (
        (
            "Банер",
            {
                "fields": ("hero_title", "hero_lead"),
                "description": "Перший екран головної.",
            },
        ),
        (
            "Напрями",
            {
                "fields": ("directions_kicker", "directions_title", "directions_lead"),
                "description": "Заголовки секції. Самі послуги — у пункті «Послуги».",
            },
        ),
        (
            "Чому з нами",
            {
                "fields": (
                    "why_kicker",
                    "why_title",
                    "why_lead",
                    "why_1_title",
                    "why_1_body",
                    "why_2_title",
                    "why_2_body",
                    "why_3_title",
                    "why_3_body",
                )
            },
        ),
        (
            "Новини на головній",
            {
                "fields": ("news_kicker", "news_title"),
                "description": "Заголовок стрічки. Самі новини — у пункті «Новини».",
            },
        ),
        ("SEO", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )


@admin.register(AboutPage)
class AboutPageAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("lead", "story")
    inlines = (TeamMemberInline, CaseInline, CertificateInline)
    fieldsets = (
        (
            "Вступ",
            {
                "fields": ("lead",),
                "description": "Команда, кейси і сертифікати — таблиці внизу форми.",
            },
        ),
        ("Хто ми", {"fields": ("story",)}),
        (
            "Цифри",
            {
                "fields": (
                    "stat_1_value",
                    "stat_1_label",
                    "stat_2_value",
                    "stat_2_label",
                    "stat_3_value",
                    "stat_3_label",
                    "stat_4_value",
                    "stat_4_label",
                )
            },
        ),
        (
            "Сертифікати",
            {
                "fields": ("certs_kicker", "certs_title", "certs_lead"),
                "description": "Заголовки секції. Скани додайте в таблиці «Сертифікати» нижче.",
            },
        ),
        ("SEO", {"fields": ("meta_title", "meta_description"), "classes": ("collapse",)}),
    )
