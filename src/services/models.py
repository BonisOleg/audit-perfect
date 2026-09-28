from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from src.core.l10n import bind_localized, brand_name, localized


class Service(models.Model):
    title_uk = models.CharField("Назва", max_length=160)
    title_en = models.CharField("Title", max_length=160, blank=True)
    slug = models.SlugField("Slug", unique=True, max_length=80)
    short_description_uk = models.CharField("Короткий опис", max_length=255)
    short_description_en = models.CharField("Short description", max_length=255, blank=True)
    audience_uk = models.CharField("Для кого", max_length=400, blank=True)
    audience_en = models.CharField("Audience", max_length=400, blank=True)
    body_uk = models.TextField("Опис", blank=True)
    body_en = models.TextField("Description", blank=True)
    composition_uk = models.JSONField("Склад", default=list, blank=True)
    composition_en = models.JSONField("Composition", default=list, blank=True)
    meta_title_uk = models.CharField("SEO title", max_length=70, blank=True)
    meta_title_en = models.CharField("SEO title", max_length=70, blank=True)
    meta_description_uk = models.CharField("SEO description", max_length=160, blank=True)
    meta_description_en = models.CharField("SEO description", max_length=160, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"
        ordering = ["sort_order", "title_uk"]

    def __str__(self) -> str:
        return self.title_uk or self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_uk or self.title_en, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("services:detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self) -> str:
        meta = (localized(self, "meta_title") or "").strip()
        name = (localized(self, "title") or "").strip()
        brand = brand_name()
        return meta or (f"{name} — {brand}" if name else brand)

    @property
    def seo_description(self) -> str:
        return (localized(self, "meta_description") or "").strip() or (
            localized(self, "short_description") or ""
        )

    @property
    def composition(self):
        value = localized(self, "composition")
        return value if isinstance(value, list) else []

    @property
    def audience_body(self) -> str:
        text = (localized(self, "audience") or "").strip()
        for prefix in ("Для кого: ", "Для кого:"):
            if text.startswith(prefix):
                text = text[len(prefix) :].lstrip()
                break
        if not text:
            return ""
        return text[:1].upper() + text[1:]


bind_localized(
    Service,
    (
        "title",
        "short_description",
        "audience",
        "body",
        "meta_title",
        "meta_description",
    ),
)
