from django.db import models

from src.core.l10n import bind_localized
from src.core.models import SiteSettings


class SiteBlock(models.Model):
    class Page(models.TextChoices):
        HOME = "home", "Головна"
        ABOUT = "about", "Про нас"

    class BlockType(models.TextChoices):
        TEXT = "text", "Текст"
        HTML = "html", "HTML"
        IMAGE = "image", "Зображення"

    page = models.CharField(
        "Сторінка",
        max_length=64,
        choices=Page.choices,
        db_index=True,
    )
    key = models.CharField(
        "Ключ",
        max_length=64,
        help_text="Не змінюйте ключ, якщо блок уже на сайті.",
    )
    title = models.CharField("Заголовок", max_length=255, blank=True)
    body = models.TextField("Текст", blank=True)
    image = models.ImageField("Зображення", upload_to="blocks/", blank=True)
    block_type = models.CharField(
        "Тип",
        max_length=16,
        choices=BlockType.choices,
        default=BlockType.TEXT,
    )
    is_visible = models.BooleanField("Видимий", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Текст сторінки"
        verbose_name_plural = "Тексти сторінок"
        ordering = ["page", "sort_order", "key"]
        constraints = [
            models.UniqueConstraint(fields=["page", "key"], name="uniq_siteblock_page_key"),
        ]

    def __str__(self) -> str:
        return f"{self.page}:{self.key}"


bind_localized(
    SiteSettings,
    (
        "site_name",
        "tagline",
        "legal_name",
        "address",
        "hours_weekdays",
        "hours_weekend",
        "hours_note",
        "visit_directions",
        "footer_blurb",
        "consult_kicker",
        "consult_title",
        "default_meta_title",
        "default_meta_description",
        "home_meta_title",
        "home_meta_description",
        "about_meta_title",
        "about_meta_description",
        "contacts_meta_title",
        "contacts_meta_description",
        "policy_meta_title",
        "policy_meta_description",
        "services_meta_title",
        "services_meta_description",
        "news_meta_title",
        "news_meta_description",
        "policy_body",
    ),
)
