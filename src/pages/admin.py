from django.contrib import admin
from unfold.admin import StackedInline

from src.core.admin_mixins import TinyMceBodyMixin
from src.core.admin_singleton import SingletonAdmin
from src.pages.models import AboutPage, Certificate, HeroSlide, HomePage
from src.team.admin import CaseInline, TeamMemberInline


class HeroSlideInline(StackedInline):
    model = HeroSlide
    extra = 4
    can_delete = True
    fields = ("image", "sort_order", "is_active")
    ordering = ("sort_order", "id")


class CertificateInline(StackedInline):
    model = Certificate
    extra = 0
    can_delete = True
    tab = True
    ordering = ("sort_order", "id")
    fieldsets = (
        (
            "Спільне",
            {"fields": ("image", "sort_order", "is_active")},
        ),
        (
            "Українська",
            {"fields": ("title_uk",)},
        ),
        (
            "English",
            {"fields": ("title_en",)},
        ),
    )


@admin.register(HomePage)
class HomePageAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("hero_title_uk", "hero_title_en", "hero_lead_uk", "hero_lead_en")
    inlines = (HeroSlideInline,)
    fieldsets = (
        (
            "Спільне",
            {
                "classes": ["tab"],
                "fields": ("hero_mode", "hero_image", "hero_video", "hero_poster"),
                "description": (
                    "Режим «Слайдер» бере фото з блоку «Фото слайдера». "
                    "На сайті слайдер вмикається від двох фото. "
                    "Відео — MP4 без звуку; на проді файл до 20 МБ."
                ),
            },
        ),
        (
            "Українська",
            {
                "classes": ["tab"],
                "fields": (
                    "hero_title_uk",
                    "hero_lead_uk",
                    "directions_kicker_uk",
                    "directions_title_uk",
                    "directions_lead_uk",
                    "why_kicker_uk",
                    "why_title_uk",
                    "why_lead_uk",
                    "why_1_title_uk",
                    "why_1_body_uk",
                    "why_2_title_uk",
                    "why_2_body_uk",
                    "why_3_title_uk",
                    "why_3_body_uk",
                    "news_kicker_uk",
                    "news_title_uk",
                    "meta_title_uk",
                    "meta_description_uk",
                ),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": (
                    "hero_title_en",
                    "hero_lead_en",
                    "directions_kicker_en",
                    "directions_title_en",
                    "directions_lead_en",
                    "why_kicker_en",
                    "why_title_en",
                    "why_lead_en",
                    "why_1_title_en",
                    "why_1_body_en",
                    "why_2_title_en",
                    "why_2_body_en",
                    "why_3_title_en",
                    "why_3_body_en",
                    "news_kicker_en",
                    "news_title_en",
                    "meta_title_en",
                    "meta_description_en",
                ),
            },
        ),
    )


@admin.register(AboutPage)
class AboutPageAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("lead_uk", "lead_en", "story_uk", "story_en")
    inlines = (TeamMemberInline, CaseInline, CertificateInline)
    fieldsets = (
        (
            "Спільне",
            {
                "classes": ["tab"],
                "fields": ("stat_1_value", "stat_2_value", "stat_3_value", "stat_4_value"),
                "description": "Лише цифри. Підписи до них — у вкладках мов. Команда, кейси і сертифікати — окремі вкладки зверху.",
            },
        ),
        (
            "Українська",
            {
                "classes": ["tab"],
                "fields": (
                    "lead_uk",
                    "story_uk",
                    "stat_1_label_uk",
                    "stat_2_label_uk",
                    "stat_3_label_uk",
                    "stat_4_label_uk",
                    "certs_kicker_uk",
                    "certs_title_uk",
                    "certs_lead_uk",
                    "meta_title_uk",
                    "meta_description_uk",
                ),
            },
        ),
        (
            "English",
            {
                "classes": ["tab"],
                "fields": (
                    "lead_en",
                    "story_en",
                    "stat_1_label_en",
                    "stat_2_label_en",
                    "stat_3_label_en",
                    "stat_4_label_en",
                    "certs_kicker_en",
                    "certs_title_en",
                    "certs_lead_en",
                    "meta_title_en",
                    "meta_description_en",
                ),
            },
        ),
    )
