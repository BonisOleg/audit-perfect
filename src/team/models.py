from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save


class TeamMember(models.Model):
    about = models.ForeignKey(
        "pages.AboutPage",
        on_delete=models.CASCADE,
        related_name="members",
        default=1,
    )
    name = models.CharField("Імʼя", max_length=120)
    role = models.TextField("Посада / опис")
    photo = models.ImageField(
        "Фото",
        upload_to="team/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
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


def _drop_replaced_team_photo(sender, instance, **kwargs):
    if not instance.pk:
        return
    previous = sender.objects.filter(pk=instance.pk).only("photo").first()
    if previous is None or not previous.photo:
        return
    new_name = instance.photo.name if instance.photo else ""
    if previous.photo.name != new_name:
        previous.photo.delete(save=False)


def _drop_team_photo_file(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)


pre_save.connect(
    _drop_replaced_team_photo,
    sender=TeamMember,
    dispatch_uid="team.member.photo.replace",
)
post_delete.connect(
    _drop_team_photo_file,
    sender=TeamMember,
    dispatch_uid="team.member.photo.delete",
)
