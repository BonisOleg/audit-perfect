from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField("Назва", max_length=160)
    slug = models.SlugField("Slug", unique=True, max_length=80)
    short_description = models.CharField("Короткий опис", max_length=255)
    audience = models.CharField("Для кого", max_length=400, blank=True)
    body = models.TextField("Опис", blank=True)
    composition = models.JSONField("Склад", default=list, blank=True)
    meta_title = models.CharField("SEO title", max_length=70, blank=True)
    meta_description = models.CharField("SEO description", max_length=160, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"
        ordering = ["sort_order", "title"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("services:detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self) -> str:
        return self.meta_title or f"{self.title} — Аудит-Перфект"

    @property
    def seo_description(self) -> str:
        return self.meta_description or self.short_description

    @property
    def audience_body(self) -> str:
        text = (self.audience or "").strip()
        for prefix in ("Для кого: ", "Для кого:"):
            if text.startswith(prefix):
                text = text[len(prefix) :].lstrip()
                break
        if not text:
            return ""
        return text[:1].upper() + text[1:]
