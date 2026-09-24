from django.apps import AppConfig
from django.db.models.signals import pre_save


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"
    label = "core"
    verbose_name = "Сайт"

    def ready(self) -> None:
        from src.core.images import convert_uploaded_images

        pre_save.connect(
            convert_uploaded_images,
            dispatch_uid="core.images.webp",
        )
