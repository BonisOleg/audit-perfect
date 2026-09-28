from urllib.parse import urlsplit, urlunsplit

from django.conf import settings


def prefixed_codes() -> tuple[str, ...]:
    return tuple(code for code, _label in settings.LANGUAGES if code != settings.LANGUAGE_CODE)


def strip_language_prefix(path: str) -> str:
    parts = urlsplit(path)
    segments = (parts.path or "/").split("/")
    prefixes = set(prefixed_codes())
    while len(segments) > 1 and segments[1] in prefixes:
        del segments[1]
    new_path = "/".join(segments) or "/"
    if not new_path.startswith("/"):
        new_path = f"/{new_path}"
    return urlunsplit(("", "", new_path, parts.query, ""))


def localize_path(path: str, lang: str) -> str:
    stripped = strip_language_prefix(path)
    parts = urlsplit(stripped)
    clean = parts.path or "/"
    if not clean.startswith("/"):
        clean = f"/{clean}"
    if lang == settings.LANGUAGE_CODE or lang not in prefixed_codes():
        target = clean
    elif clean == "/":
        target = f"/{lang}/"
    else:
        target = f"/{lang}{clean}"
    return urlunsplit(("", "", target, parts.query, ""))


def collapse_double_prefix(path: str) -> str:
    parts = urlsplit(path)
    segments = (parts.path or "/").split("/")
    prefixes = set(prefixed_codes())
    changed = False
    while len(segments) > 2 and segments[1] in prefixes and segments[2] in prefixes:
        del segments[1]
        changed = True
    if not changed:
        return path
    new_path = "/".join(segments) or "/"
    if not new_path.startswith("/"):
        new_path = f"/{new_path}"
    return urlunsplit(("", "", new_path, parts.query, ""))
