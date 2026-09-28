from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from django.views.decorators.http import require_POST

from src.core.i18n import collapse_double_prefix, localize_path
from src.core.middleware import english_is_public


def _extract_next(request) -> str:
    candidate = (request.POST.get("next") or request.META.get("HTTP_REFERER") or "/").strip()
    if not candidate:
        return "/"
    if candidate.startswith("/") and not candidate.startswith("//"):
        parts = urlsplit(candidate)
        query = f"?{parts.query}" if parts.query else ""
        return f"{parts.path or '/'}{query}"
    if url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        parts = urlsplit(candidate)
        query = f"?{parts.query}" if parts.query else ""
        return f"{parts.path or '/'}{query}"
    return "/"


@require_POST
def set_language(request):
    lang = (request.POST.get("language") or "").strip()
    if not check_for_language(lang):
        lang = settings.LANGUAGE_CODE
    if lang != settings.LANGUAGE_CODE and not english_is_public():
        lang = settings.LANGUAGE_CODE
    target = collapse_double_prefix(localize_path(_extract_next(request), lang))
    response = HttpResponseRedirect(target)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response
