from pathlib import Path

from django.conf import settings
from django.utils.translation import get_language

from src.core.i18n import localize_path
from src.core.models import SiteSettings
from src.services.models import Service


def _static_asset_version() -> int:
    static_root = Path(settings.BASE_DIR) / "src" / "core" / "static"
    mtimes = [
        int(p.stat().st_mtime)
        for pattern in (
            "css/**/*.css",
            "js/**/*.js",
            "images/favicon*",
            "images/apple-touch-icon.png",
        )
        for p in static_root.glob(pattern)
    ]
    return max(mtimes) if mtimes else 0


def site_globals(request):
    site = SiteSettings.load()
    services = Service.objects.filter(is_active=True).order_by("sort_order")
    url_name = ""
    if getattr(request, "resolver_match", None):
        url_name = request.resolver_match.url_name or ""
    path = request.get_full_path()
    language = (get_language() or settings.LANGUAGE_CODE).split("-")[0]
    return {
        "site": site,
        "nav_services": services,
        "is_homepage": url_name == "home",
        "site_url": settings.SITE_URL,
        "ga4_id": settings.GA4_MEASUREMENT_ID,
        "current_nav": getattr(request, "current_nav", ""),
        "static_version": _static_asset_version(),
        "current_language": language,
        "en_enabled": bool(site.en_enabled),
        "lang_switch_urls": {
            "uk": localize_path(path, "uk"),
            "en": localize_path(path, "en"),
        },
    }
