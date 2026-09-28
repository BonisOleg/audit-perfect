from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import SafeString
from django.utils.text import slugify

from src.core.l10n import bind_localized, brand_name, localized
from src.core.richtext import render_cms_text


class News(models.Model):
    title_uk = models.CharField("Заголовок", max_length=200)
    title_en = models.CharField("Title", max_length=200, blank=True)
    slug = models.SlugField("Slug", unique=True, max_length=200)
    excerpt_uk = models.CharField("Анонс", max_length=300, blank=True)
    excerpt_en = models.CharField("Excerpt", max_length=300, blank=True)
    body_uk = models.TextField("Текст")
    body_en = models.TextField("Body", blank=True)
    published_at = models.DateTimeField("Дата публікації", default=timezone.now)
    is_published = models.BooleanField("Опубліковано", default=True)
    meta_title_uk = models.CharField("SEO title", max_length=70, blank=True)
    meta_title_en = models.CharField("SEO title", max_length=70, blank=True)
    meta_description_uk = models.CharField("SEO description", max_length=160, blank=True)
    meta_description_en = models.CharField("SEO description", max_length=160, blank=True)

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title_uk or self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_uk or self.title_en, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self) -> str:
        meta = (localized(self, "meta_title") or "").strip()
        name = (localized(self, "title") or "").strip()
        brand = brand_name()
        return meta or (f"{name} — {brand}" if name else brand)

    @property
    def seo_description(self) -> str:
        return (localized(self, "meta_description") or "").strip() or (localized(self, "excerpt") or "")

    @property
    def body_html(self) -> SafeString:
        return render_cms_text(localized(self, "body"))


bind_localized(News, ("title", "excerpt", "body", "meta_title", "meta_description"))
