from django.conf import settings

from src.core.models import SiteSettings
from src.services.models import Service


def site_globals(request):
    site = SiteSettings.load()
    services = Service.objects.filter(is_active=True).order_by("sort_order")
    url_name = ""
    if getattr(request, "resolver_match", None):
        url_name = request.resolver_match.url_name or ""
    return {
        "site": site,
        "nav_services": services,
        "is_homepage": url_name == "home",
        "site_url": settings.SITE_URL,
        "ga4_id": settings.GA4_MEASUREMENT_ID,
        "current_nav": getattr(request, "current_nav", ""),
    }
