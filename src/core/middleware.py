from django.db.utils import OperationalError, ProgrammingError
from django.http import HttpResponseRedirect

from src.core.i18n import collapse_double_prefix, localize_path, prefixed_codes


def english_is_public() -> bool:
    from src.core.models import SiteSettings

    try:
        return bool(SiteSettings.load().en_enabled)
    except (OperationalError, ProgrammingError):
        return True


class LanguagePrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        full = request.get_full_path()
        collapsed = collapse_double_prefix(full)
        if collapsed != full:
            return HttpResponseRedirect(collapsed)
        path = request.path_info or "/"
        prefix = path.strip("/").split("/", 1)[0]
        if prefix in prefixed_codes() and not english_is_public():
            return HttpResponseRedirect(localize_path(full, "uk"))
        return self.get_response(request)
