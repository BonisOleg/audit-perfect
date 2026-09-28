from django.utils.translation import get_language


def brand_name() -> str:
    from src.core.models import SiteSettings

    value = (localized(SiteSettings.load(), "site_name") or "").strip()
    return value or "Аудит-Перфект"


def localized(obj, field: str, language: str | None = None):
    """Поле поточною мовою. Для en порожнє значення не замінюється українським."""
    lang = (language or get_language() or "uk").split("-")[0]
    if lang not in {"uk", "en"}:
        lang = "uk"
    value = getattr(obj, f"{field}_{lang}", None)
    if value is None:
        return ""
    return value


class Localized:
    def __init__(self, name: str):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return localized(obj, self.name)


def bind_localized(cls, names: tuple[str, ...]) -> None:
    for name in names:
        setattr(cls, name, Localized(name))
