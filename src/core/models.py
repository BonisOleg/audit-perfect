from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField("Назва", max_length=120, default="Аудит-Перфект")
    tagline = models.CharField("Підпис", max_length=120, default="Аудиторська фірма")
    legal_name = models.CharField(
        "Юридична назва",
        max_length=255,
        default="ПП «АФ «Аудит-Перфект»»",
        blank=True,
    )
    edrpou = models.CharField("ЄДРПОУ", max_length=20, default="34971458", blank=True)
    phone = models.CharField("Телефон", max_length=40, default="+38 044 355 18 22")
    phone_href = models.CharField("tel:", max_length=40, default="+380443551822")
    phone_secondary = models.CharField(
        "Додатковий телефон",
        max_length=40,
        blank=True,
        default="",
    )
    phone_secondary_href = models.CharField(
        "tel: (додатковий)",
        max_length=40,
        blank=True,
        default="",
    )
    telegram = models.CharField(
        "Telegram",
        max_length=80,
        blank=True,
        default="",
        help_text="Username без @ або повне посилання t.me/…",
    )
    email = models.EmailField("Email", default="office@auditperfekt.ua")
    address = models.CharField(
        "Адреса",
        max_length=255,
        default="вул. Велика Житомирська, 20, Київ",
    )
    map_embed_url = models.URLField("Карта (embed)", blank=True)
    maps_url = models.URLField(
        "Посилання на карту (Google/Apple)",
        blank=True,
        help_text="Якщо порожньо — будується з адреси.",
    )
    hours_weekdays = models.CharField(
        "Години Пн–Пт",
        max_length=80,
        default="09:00–18:00",
    )
    hours_weekend = models.CharField(
        "Години Сб–Нд",
        max_length=80,
        default="Вихідний",
    )
    hours_note = models.CharField(
        "Примітка до графіка",
        max_length=255,
        blank=True,
        default="Обідня перерва 13:00–14:00.",
    )
    visit_directions = models.TextField(
        "Як дістатися",
        blank=True,
        default=(
            "Метро «Золоті ворота» — 7–8 хвилин пішки\n"
            "Вхід з боку вул. Велика Житомирська\n"
            "Паркування поруч обмежене — зручніше таксі або метро"
        ),
        help_text="Кожен рядок — окремий пункт.",
    )
    registry_url = models.URLField(
        "Реєстр аудиторів",
        default="https://register.apob.org.ua/uk/search",
        blank=True,
    )
    registry_number = models.CharField("Номер у реєстрі", max_length=40, default="3975")
    default_meta_title = models.CharField(
        "SEO title за замовчуванням",
        max_length=70,
        default="Аудит-Перфект — аудит, облік і супровід бізнесу",
    )
    default_meta_description = models.CharField(
        "SEO description за замовчуванням",
        max_length=160,
        default=(
            "Супроводжуємо бізнес у звітності, перевірках "
            "і призначенні статусу критично важливого підприємства."
        ),
    )

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self) -> str:
        return self.site_name

    @classmethod
    def load(cls) -> "SiteSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def maps_link(self) -> str:
        if self.maps_url:
            return self.maps_url
        from urllib.parse import quote

        return f"https://maps.google.com/?q={quote(self.address)}"

    @property
    def telegram_url(self) -> str:
        value = (self.telegram or "").strip()
        if not value:
            return ""
        if value.startswith(("http://", "https://")):
            return value
        return f"https://t.me/{value.lstrip('@')}"

    @property
    def telegram_label(self) -> str:
        value = (self.telegram or "").strip()
        if not value:
            return ""
        if value.startswith(("http://", "https://")):
            return "Telegram"
        return f"@{value.lstrip('@')}"

    @property
    def visit_direction_lines(self) -> list[str]:
        return [
            line.strip()
            for line in (self.visit_directions or "").splitlines()
            if line.strip()
        ]


class SiteBlock(models.Model):
    class BlockType(models.TextChoices):
        TEXT = "text", "Текст"
        HTML = "html", "HTML"
        IMAGE = "image", "Зображення"

    page = models.CharField("Сторінка", max_length=64, db_index=True)
    key = models.CharField("Ключ", max_length=64)
    title = models.CharField("Заголовок", max_length=255, blank=True)
    body = models.TextField("Текст", blank=True)
    image = models.ImageField("Зображення", upload_to="blocks/", blank=True)
    block_type = models.CharField(
        max_length=16,
        choices=BlockType.choices,
        default=BlockType.TEXT,
    )
    is_visible = models.BooleanField("Видимий", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "CMS-блок"
        verbose_name_plural = "CMS-блоки"
        ordering = ["page", "sort_order", "key"]
        constraints = [
            models.UniqueConstraint(fields=["page", "key"], name="uniq_siteblock_page_key"),
        ]

    def __str__(self) -> str:
        return f"{self.page}:{self.key}"
