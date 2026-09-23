from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.safestring import SafeString

from src.core.richtext import render_cms_inline, render_cms_text


class SingletonMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


_IMAGE_EXTS = ["jpg", "jpeg", "png", "webp"]


class HomePage(SingletonMixin):
    class HeroMode(models.TextChoices):
        IMAGE = "image", "Одне зображення"
        SLIDER = "slider", "Слайдер"
        VIDEO = "video", "Відео"

    hero_mode = models.CharField(
        "Режим банера",
        max_length=16,
        choices=HeroMode.choices,
        default=HeroMode.IMAGE,
    )
    hero_image = models.ImageField(
        "Зображення банера",
        upload_to="hero/",
        blank=True,
        validators=[FileExtensionValidator(_IMAGE_EXTS)],
    )
    hero_video = models.FileField(
        "Відео банера",
        upload_to="hero/video/",
        blank=True,
        validators=[FileExtensionValidator(["mp4"])],
        help_text="MP4 без звуку, короткий цикл. На проді nginx приймає файл до 20 МБ.",
    )
    hero_poster = models.ImageField(
        "Кадр до старту відео",
        upload_to="hero/poster/",
        blank=True,
        validators=[FileExtensionValidator(_IMAGE_EXTS)],
        help_text="Показується, поки відео вантажиться, і якщо в системі увімкнено «зменшити рух».",
    )
    hero_title = models.TextField(
        "Слоган",
        default=(
            "Супроводжуємо бізнес у звітності, перевірках "
            "і призначенні статусу критично важливого підприємства."
        ),
    )
    hero_lead = models.TextField(
        "Підзаголовок банера",
        default=(
            "Аудит, облік, трансфертне ціноутворення, КІК, "
            "військовий облік і юридичний супровід — однією командою."
        ),
    )
    why_1_title = models.CharField("Перевага 1 — заголовок", max_length=120, default="Одна команда")
    why_1_body = models.CharField(
        "Перевага 1 — текст",
        max_length=255,
        default="Одна команда веде справу до досягнення мети.",
    )
    why_2_title = models.CharField(
        "Перевага 2 — заголовок",
        max_length=120,
        default="Статус критичності",
    )
    why_2_body = models.CharField(
        "Перевага 2 — текст",
        max_length=255,
        default="Супровід на кожному етапі до позитивного результату.",
    )
    why_3_title = models.CharField(
        "Перевага 3 — заголовок",
        max_length=120,
        default="Супровід перевірок",
    )
    why_3_body = models.CharField(
        "Перевага 3 — текст",
        max_length=255,
        default="Звільняємо бізнес від зайвої витрати часу та нервів.",
    )
    directions_kicker = models.CharField("Напрями — підпис", max_length=80, default="Сім напрямів")
    directions_title = models.CharField("Напрями — заголовок", max_length=120, default="Напрями роботи")
    directions_lead = models.CharField(
        "Напрями — текст",
        max_length=255,
        default="Комплексний супровід бізнесу в одній команді. Деталі напрямів — у каталозі.",
    )
    why_kicker = models.CharField("Чому з нами — підпис", max_length=80, default="Підхід")
    why_title = models.CharField("Чому з нами — заголовок", max_length=120, default="Чому з нами")
    why_lead = models.CharField(
        "Чому з нами — лід",
        max_length=255,
        default="Одна команда веде справу до досягнення мети.",
    )
    news_kicker = models.CharField("Новини — підпис", max_length=80, default="Стрічка")
    news_title = models.CharField("Новини — заголовок", max_length=120, default="Новини")
    meta_title = models.CharField(
        "SEO title",
        max_length=70,
        blank=True,
        default="Аудит-Перфект — аудит, облік і супровід бізнесу",
    )
    meta_description = models.CharField(
        "SEO description",
        max_length=160,
        blank=True,
        default=(
            "Супроводжуємо бізнес у звітності, перевірках "
            "і призначенні статусу критично важливого підприємства."
        ),
    )

    class Meta:
        verbose_name = "Головна"
        verbose_name_plural = "Головна"

    def __str__(self) -> str:
        return "Головна"

    @property
    def hero_title_html(self) -> SafeString:
        return render_cms_inline(self.hero_title)

    @property
    def hero_lead_html(self) -> SafeString:
        return render_cms_text(self.hero_lead)

    @property
    def why_items(self) -> list[dict[str, str]]:
        items = []
        for index in (1, 2, 3):
            title = (getattr(self, f"why_{index}_title") or "").strip()
            body = (getattr(self, f"why_{index}_body") or "").strip()
            if title or body:
                items.append({"title": title, "body": body})
        return items

    def hero_media(self) -> dict:
        slides = [
            slide.image.url
            for slide in self.hero_slides.filter(is_active=True).order_by("sort_order", "id")
            if slide.image
        ]
        image = self.hero_image.url if self.hero_image else ""
        poster = self.hero_poster.url if self.hero_poster else ""
        video = self.hero_video.url if self.hero_video else ""
        if self.hero_mode == self.HeroMode.VIDEO and video:
            return {"kind": "video", "video": video, "poster": poster or image}
        if self.hero_mode == self.HeroMode.SLIDER and len(slides) >= 2:
            return {"kind": "slider", "slides": slides}
        if self.hero_mode == self.HeroMode.SLIDER and len(slides) == 1:
            image = slides[0]
        elif self.hero_mode == self.HeroMode.VIDEO:
            image = poster or image
        return {"kind": "image", "image": image}


class HeroSlide(models.Model):
    home = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="hero_slides",
        default=1,
    )
    image = models.ImageField(
        "Зображення",
        upload_to="hero/slides/",
        validators=[FileExtensionValidator(_IMAGE_EXTS)],
    )
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показувати", default=True)

    class Meta:
        verbose_name = "фото слайдера"
        verbose_name_plural = "Фото слайдера"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"Слайд {self.sort_order}"


class AboutPage(SingletonMixin):
    lead = models.TextField(
        "Лід під заголовком",
        default=(
            "Працюємо з власниками бізнесу, фінансовими директорами та "
            "групами компаній, яким потрібна прозора звітність "
            "і конструктивний діалог з контролюючими органами."
        ),
    )
    story = models.TextField("Текст «Хто ми»", blank=True)
    stat_1_value = models.CharField("Цифра 1", max_length=20, default="19")
    stat_1_label = models.CharField("Підпис 1", max_length=120, default="років на ринку")
    stat_2_value = models.CharField("Цифра 2", max_length=20, default="500")
    stat_2_label = models.CharField("Підпис 2", max_length=120, default="постійних клієнтів")
    stat_3_value = models.CharField("Цифра 3", max_length=20, default="25")
    stat_3_label = models.CharField(
        "Підпис 3",
        max_length=160,
        default="успішних проєктів зі статусом критичності",
    )
    stat_4_value = models.CharField("Цифра 4", max_length=20, default="50")
    stat_4_label = models.CharField("Підпис 4", max_length=120, default="супроводжених аудитів")
    certs_kicker = models.CharField("Сертифікати — підпис", max_length=80, default="Допуски")
    certs_title = models.CharField("Сертифікати — заголовок", max_length=120, default="Сертифікати")
    certs_lead = models.CharField(
        "Сертифікати — текст",
        max_length=255,
        default="Реєстр аудиторів та документи фірми.",
    )
    meta_title = models.CharField(
        "SEO title",
        max_length=70,
        blank=True,
        default="Про нас — Аудит-Перфект",
    )
    meta_description = models.CharField(
        "SEO description",
        max_length=160,
        blank=True,
        default=(
            "ПП «АФ «Аудит-Перфект»»: аудит, облік, ТЦ, КІК, військовий облік "
            "та юридичний супровід з 2007 року."
        ),
    )

    class Meta:
        verbose_name = "Про нас"
        verbose_name_plural = "Про нас"

    def __str__(self) -> str:
        return "Про нас"

    @property
    def lead_html(self) -> SafeString:
        return render_cms_text(self.lead)

    @property
    def story_html(self) -> SafeString:
        return render_cms_text(self.story)

    @property
    def stat_items(self) -> list[dict[str, str]]:
        items = []
        for index in (1, 2, 3, 4):
            value = (getattr(self, f"stat_{index}_value") or "").strip()
            label = (getattr(self, f"stat_{index}_label") or "").strip()
            if value or label:
                items.append({"value": value, "label": label})
        return items


class Certificate(models.Model):
    about = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="certificates",
        default=1,
    )
    title = models.CharField("Підпис", max_length=200)
    image = models.ImageField(
        "Скан / фото",
        upload_to="certs/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показувати", default=True)

    class Meta:
        verbose_name = "Сертифікат"
        verbose_name_plural = "Сертифікати"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.title


def _stored_name(field_file) -> str:
    if not field_file:
        return ""
    return field_file.name or ""


def _drop_replaced_file(old_file, new_file) -> None:
    old_name = _stored_name(old_file)
    new_name = _stored_name(new_file)
    if old_name and old_name != new_name:
        old_file.delete(save=False)


def _drop_replaced_homepage_files(sender, instance, **kwargs):
    if not instance.pk:
        return
    previous = sender.objects.filter(pk=instance.pk).first()
    if previous is None:
        return
    for field_name in ("hero_image", "hero_video", "hero_poster"):
        _drop_replaced_file(getattr(previous, field_name), getattr(instance, field_name))


def _drop_replaced_hero_slide(sender, instance, **kwargs):
    if not instance.pk:
        return
    previous = sender.objects.filter(pk=instance.pk).only("image").first()
    if previous is None:
        return
    _drop_replaced_file(previous.image, instance.image)


def _drop_hero_slide_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


pre_save.connect(
    _drop_replaced_homepage_files,
    sender=HomePage,
    dispatch_uid="pages.home.hero.files",
)
pre_save.connect(
    _drop_replaced_hero_slide,
    sender=HeroSlide,
    dispatch_uid="pages.hero.slide.replace",
)
post_delete.connect(
    _drop_hero_slide_file,
    sender=HeroSlide,
    dispatch_uid="pages.hero.slide.delete",
)
