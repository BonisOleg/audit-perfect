import re

_HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")

DEFAULT_RED = "#ec423c"
DEFAULT_BLUE = "#002fa7"
DEFAULT_INK = "#141824"
DEFAULT_BG = "#ffffff"
DEFAULT_WASH = "#f7f6f3"


def normalize_hex(value: str, fallback: str) -> str:
    text = (value or "").strip()
    if _HEX.fullmatch(text):
        return text.lower()
    return fallback


def _rgb(value: str) -> tuple[int, int, int]:
    return int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16)


def _hex(red: float, green: float, blue: float) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, round(red))),
        max(0, min(255, round(green))),
        max(0, min(255, round(blue))),
    )


def mix(origin: str, target: str, amount: float) -> str:
    origin_rgb = _rgb(origin)
    target_rgb = _rgb(target)
    return _hex(
        *(
            channel + (toward - channel) * amount
            for channel, toward in zip(origin_rgb, target_rgb)
        )
    )


def darken(value: str, amount: float) -> str:
    return mix(value, "#000000", amount)


def build_theme_css(
    red: str,
    blue: str,
    ink: str,
    bg: str,
    wash: str,
    font_display: str = '"Onest","Helvetica Neue",sans-serif',
    font_body: str = '"Manrope","Helvetica Neue",sans-serif',
) -> str:
    red = normalize_hex(red, DEFAULT_RED)
    blue = normalize_hex(blue, DEFAULT_BLUE)
    ink = normalize_hex(ink, DEFAULT_INK)
    bg = normalize_hex(bg, DEFAULT_BG)
    wash = normalize_hex(wash, DEFAULT_WASH)
    variables = {
        "--red": red,
        "--red-deep": darken(red, 0.16),
        "--blue": blue,
        "--ink": ink,
        "--bg": bg,
        "--wash": wash,
        "--muted": mix(ink, bg, 0.34),
        "--line": mix(bg, ink, 0.08),
        "--btn": ink,
        "--btn-hover": mix(ink, "#ffffff", 0.12),
        "--on-btn": bg,
        "--hero": darken(ink, 0.45),
        "--ff-display": font_display,
        "--ff-body": font_body,
    }
    body = "".join(f"{name}:{value};" for name, value in variables.items())
    return f":root{{{body}}}"
