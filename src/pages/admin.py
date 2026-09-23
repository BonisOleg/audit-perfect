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
    extra = 1
    fields = ("title", "image", "sort_order", "is_active")
    ordering = ("sort_order", "id")


@admin.register(HomePage)
class HomePageAdmin(TinyMceBodyMixin, SingletonAdmin):
    tinymce_fields = ("hero_title", "hero_lead")
    inlines = (HeroSlideInline,)
    fieldsets = (
        (
            "Банер",
            {
                "fields": (
                    "hero_mode",
                    "hero_image",
                    "hero_video",
                    "hero_poster",
                ),
                "description": (
                    "Режим «Слайдер» бере фото з блоку «Фото слайдера» одразу нижче. "
                    "Там два порожні поля і кнопка «Додати ще…» для третього і наступних. "
                    "На сайті слайдер вмикається від двох фото. "
                    "Відео — MP4 без звуку; на проді файл до 20 МБ."
                ),
            },
        ),
        (
            "Текст банера",
            {"fields": ("hero_title", "hero_lead")},
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
                "description": "Команда, кейси і сертифікати — блоки нижче. Фото команди завантажується файлом.",
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
