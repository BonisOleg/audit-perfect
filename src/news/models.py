from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Slug", unique=True, max_length=200)
    excerpt = models.CharField("Анонс", max_length=300, blank=True)
    body = models.TextField("Текст")
    published_at = models.DateTimeField("Дата публікації", default=timezone.now)
    is_published = models.BooleanField("Опубліковано", default=True)
    meta_title = models.CharField("SEO title", max_length=70, blank=True)
    meta_description = models.CharField("SEO description", max_length=160, blank=True)

    class Meta:
        verbose_name = "Новина"
        verbose_name_plural = "Новини"
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def seo_title(self) -> str:
        return self.meta_title or f"{self.title} — Аудит-Перфект"

    @property
    def seo_description(self) -> str:
        return self.meta_description or self.excerpt
