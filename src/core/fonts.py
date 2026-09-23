from urllib.parse import quote

_FALLBACK = '"Helvetica Neue",sans-serif'
_WEIGHTS = "wght@400;500;600;700"

# slug, назва в адмінці, назва родини в CSS
FONTS = (
    ("onest", "Onest", "Onest"),
    ("manrope", "Manrope", "Manrope"),
    ("inter", "Inter", "Inter"),
    ("source-sans-3", "Source Sans 3", "Source Sans 3"),
    ("ibm-plex-sans", "IBM Plex Sans", "IBM Plex Sans"),
    ("nunito-sans", "Nunito Sans", "Nunito Sans"),
    ("noto-sans", "Noto Sans", "Noto Sans"),
    ("rubik", "Rubik", "Rubik"),
    ("fira-sans", "Fira Sans", "Fira Sans"),
    ("wix-madefor-text", "Wix Madefor Text", "Wix Madefor Text"),
)

FONT_CHOICES = [(slug, label) for slug, label, _family in FONTS]
_BY_SLUG = {slug: family for slug, _label, family in FONTS}

DEFAULT_DISPLAY = "onest"
DEFAULT_BODY = "manrope"


def family_name(slug: str, fallback: str) -> str:
    return _BY_SLUG.get(slug) or _BY_SLUG[fallback]


def font_stack(slug: str, fallback: str) -> str:
    return f'"{family_name(slug, fallback)}",{_FALLBACK}'


def google_fonts_href(display_slug: str, body_slug: str) -> str:
    families = []
    for slug, fallback in ((display_slug, DEFAULT_DISPLAY), (body_slug, DEFAULT_BODY)):
        name = family_name(slug, fallback)
        if name not in families:
            families.append(name)
    query = "&".join(
        "family=" + quote(name).replace("%20", "+") + ":" + _WEIGHTS for name in families
    )
    return f"https://fonts.googleapis.com/css2?{query}&display=swap"
