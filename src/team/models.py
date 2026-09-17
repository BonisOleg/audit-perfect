from django.db import models


class TeamMember(models.Model):
    about = models.ForeignKey(
        "pages.AboutPage",
        on_delete=models.CASCADE,
        related_name="members",
        default=1,
    )
    name = models.CharField("Імʼя", max_length=120)
    role = models.TextField("Посада / опис")
    photo = models.CharField(
        "Шлях static (images/...)",
        max_length=255,
        blank=True,
        help_text="Наприклад images/team/yesieva.webp",
    )
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Член команди"
        verbose_name_plural = "Команда"
        ordering = ["sort_order", "name"]

    def __str__(self) -> str:
        return self.name


class Case(models.Model):
    about = models.ForeignKey(
        "pages.AboutPage",
        on_delete=models.CASCADE,
        related_name="work_cases",
        default=1,
    )
    title = models.CharField("Назва", max_length=200)
    industry = models.CharField("Галузь", max_length=120, blank=True)
    result = models.CharField("Результат", max_length=300, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = "Кейси"
        ordering = ["sort_order", "title"]

    def __str__(self) -> str:
        return self.title
