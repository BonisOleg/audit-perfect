from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminExpandableTextareaWidget

from src.core.admin_mixins import TinyMceBodyMixin
from src.services.models import Service


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

    class Meta:
        model = Service
        exclude = ("composition",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        items = getattr(self.instance, "composition", None) or []
        if items and not self.is_bound:
            self.fields["composition_text"].initial = "\n".join(
                f"{item.get('title', '').strip()} | {item.get('text', '').strip()}"
                for item in items
                if isinstance(item, dict)
            )

    def save(self, commit=True):
        self.instance.composition = _lines_to_composition(
            self.cleaned_data.get("composition_text") or ""
        )
        return super().save(commit=commit)


@admin.register(Service)
class ServiceAdmin(TinyMceBodyMixin, ModelAdmin):
    form = ServiceAdminForm
    list_display = ("title", "slug", "sort_order", "is_active")
    list_editable = ("sort_order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description")
    fieldsets = (
        (
            "Картка",
            {"fields": ("title", "slug", "short_description", "audience", "body")},
        ),
        ("Склад", {"fields": ("composition_text",)}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
        ("Публікація", {"fields": ("sort_order", "is_active")}),
    )
