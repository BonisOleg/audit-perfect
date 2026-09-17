import re

from django.utils.html import linebreaks
from django.utils.safestring import SafeString, mark_safe

_SINGLE_P = re.compile(r"^<p>(.*)</p>$", re.IGNORECASE | re.DOTALL)


def render_cms_text(value: str) -> SafeString:
    text = value or ""
    lowered = text.lower()
    if "<p" in lowered or "<br" in lowered or "<ul" in lowered or "<ol" in lowered:
        return mark_safe(text)
    return mark_safe(linebreaks(text))


def render_cms_inline(value: str) -> SafeString:
    html = str(render_cms_text(value)).strip()
    match = _SINGLE_P.fullmatch(html)
    if match and "<p" not in match.group(1).lower():
        return mark_safe(match.group(1))
    return mark_safe(html)
