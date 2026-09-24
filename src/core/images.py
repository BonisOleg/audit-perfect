import io
from pathlib import Path

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageOps, UnidentifiedImageError

_QUALITY = 85


def _as_webp(raw: bytes) -> bytes | None:
    try:
        with Image.open(io.BytesIO(raw)) as img:
            img.load()
            img = ImageOps.exif_transpose(img)
            if img.mode == "P":
                img = img.convert("RGBA" if "transparency" in img.info else "RGB")
            elif img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", quality=_QUALITY, method=4)
    except (UnidentifiedImageError, OSError, ValueError):
        return None
    return buffer.getvalue()


def _convert_field(field_file) -> None:
    if not field_file or getattr(field_file, "_committed", True):
        return
    uploaded = field_file.file
    name = Path(getattr(uploaded, "name", "") or field_file.name or "image").name
    if name.lower().endswith(".webp"):
        return
    try:
        uploaded.seek(0)
        raw = uploaded.read()
        uploaded.seek(0)
    except (AttributeError, OSError):
        return
    data = _as_webp(raw)
    if not data:
        return
    stem = Path(name).stem or "image"
    field_file.save(f"{stem}.webp", ContentFile(data), save=False)


def convert_uploaded_images(sender, instance, raw=False, **kwargs) -> None:
    if raw:
        return
    for field in instance._meta.get_fields():
        if isinstance(field, models.ImageField):
            _convert_field(getattr(instance, field.name, None))
