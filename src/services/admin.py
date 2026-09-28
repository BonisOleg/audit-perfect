from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminExpandableTextareaWidget

from src.core.admin_mixins import TinyMceBodyMixin
from src.services.models import Service


def _composition_lines(items) -> str:
    if not items:
        return ""
    return "\n".join(
        f"{item.get('title', '').strip()} | {item.get('text', '').strip()}"
        for item in items
        if isinstance(item, dict)
    )


def _lines_to_composition(raw: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for line in (raw or "").splitlines():
        line = line.strip()
        if not line:
            continue
        if " | " in line:
            title, text = line.split(" | ", 1)
        elif "|" in line:
            title, text = line.split("|", 1)
        else:
            title, text = line, ""
        items.append({"title": title.strip(), "text": text.strip()})
    return items


class ServiceAdminForm(forms.ModelForm):
    composition_text = forms.CharField(
        label="Склад послуги",
        required=False,
        widget=UnfoldAdminExpandableTextareaWidget(attrs={"rows": 10}),
        help_text="Один пункт — один рядок: Заголовок | текст",
    )

    composition_en_text = forms.CharField(
        label="Composition",
        required=False,
        widget=UnfoldAdminExpandableTextareaWidget(attrs={"rows": 10}),
        help_text="One item per line: Title | text",
    )

    class Meta:
        model = Service
        exclude = ("composition_uk", "composition_en")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.fields["composition_text"].initial = _composition_lines(
                getattr(self.instance, "composition_uk", None)
            )
            self.fields["composition_en_text"].initial = _composition_lines(
                getattr(self.instance, "composition_en", None)
            )

    def save(self, commit=True):
        self.instance.composition_uk = _lines_to_composition(
            self.cleaned_data.get("composition_text") or ""
        )
        self.instance.composition_en = _lines_to_composition(
            self.cleaned_data.get("composition_en_text") or ""
        )
        return super().save(commit=commit)


@admin.register(Service)
class ServiceAdmin(TinyMceBodyMixin, ModelAdmin):
    form = ServiceAdminForm
    list_display = ("title_uk", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("title_uk",)}
    search_fields = ("title_uk", "title_en", "short_description_uk")
    tinymce_fields = ("body_uk", "body_en")
    fieldsets = (
        (
            "Спільне",
            {"classes": ["tab"], "fields": ("slug", "sort_order", "is_active")},
        ),
        (
            "Українська",
            {
                "classes": ["tab"],
                "fields": (
                    "title_uk",
                    "short_description_uk",
                    "audience_uk",
                    "body_uk",
                    "composition_text",
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
                    "title_en",
                    "short_description_en",
                    "audience_en",
                    "body_en",
                    "composition_en_text",
                    "meta_title_en",
                    "meta_description_en",
                ),
            },
        ),
    )
